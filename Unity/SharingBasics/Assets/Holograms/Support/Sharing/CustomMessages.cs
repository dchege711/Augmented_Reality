using Academy.HoloToolkit.Sharing;
using Academy.HoloToolkit.Unity;
using System.Collections.Generic;
using System;
using System.Diagnostics;
using UnityEngine;
using System.Collections;

public class CustomMessages : Singleton<CustomMessages>
{
    /// <summary>
    /// Message enum containing our information bytes to share.
    /// The first message type has to start with UserMessageIDStart
    /// so as not to conflict with HoloToolkit internal messages.
    /// </summary>
    public enum TestMessageID : byte
    {
        HeadTransform = MessageID.UserMessageIDStart,
        ExperimentalVector3,
        ExperimentalInt,
        StageTransform,
        Max
    }

    public enum UserMessageChannels
    {
        Anchors = MessageChannel.UserMessageChannelStart,
    }

    /// <summary>
    /// Cache the local user's ID to use when sending messages
    /// </summary>
    public long localUserID
    {
        get; set;
    }

    public delegate void MessageCallback(NetworkInMessage msg);
    private Dictionary<TestMessageID, MessageCallback> _MessageHandlers = new Dictionary<TestMessageID, MessageCallback>();
    public Dictionary<TestMessageID, MessageCallback> MessageHandlers
    {
        get
        {
            return _MessageHandlers;
        }
    }

    /// <summary>
    /// Helper object that we use to route incoming message callbacks to the member
    /// functions of this class
    /// </summary>
    NetworkConnectionAdapter connectionAdapter;

    /// <summary>
    /// Cache the connection object for the sharing service
    /// </summary>
    NetworkConnection serverConnection;

    void Start()
    {
        InitializeMessageHandlers();
    }

	// This is implemented once, at the beginning of the application
    void InitializeMessageHandlers()
    {
		// Get a reference to the (one) instance of SharingStage
        SharingStage sharingStage = SharingStage.Instance;
        if (sharingStage != null)
        {
			// If none exists, create a new server connection
            serverConnection = sharingStage.Manager.GetServerConnection();
			// Also instantiate a new NetworkConnectionAdapter() instance
            connectionAdapter = new NetworkConnectionAdapter();
        }

        connectionAdapter.MessageReceivedCallback += OnMessageReceived;

        // Cache the local user ID
        this.localUserID = SharingStage.Instance.Manager.GetLocalUser().GetID();

        for (byte index = (byte)TestMessageID.HeadTransform; index < (byte)TestMessageID.Max; index++)
        {
            if (MessageHandlers.ContainsKey((TestMessageID)index) == false)
            {
                MessageHandlers.Add((TestMessageID)index, null);
            }

            serverConnection.AddListener(index, connectionAdapter);
        }
    }

    private NetworkOutMessage CreateMessage(byte MessageType)
    {
        NetworkOutMessage msg = serverConnection.CreateMessage(MessageType);
        msg.Write(MessageType);
        // Attach userID so that the message can be traced back to the sender
        msg.Write(localUserID);
        return msg;
    }

    public void SendHeadTransform(Vector3 position, Quaternion rotation, byte HasAnchor)
    {
        // If we are connected to a session, broadcast our head info
        if (this.serverConnection != null && this.serverConnection.IsConnected())
        {
            // Create an outgoing network message to contain all the info we want to send
            NetworkOutMessage msg = CreateMessage((byte)TestMessageID.HeadTransform);

            AppendTransform(msg, position, rotation);

            msg.Write(HasAnchor);

            // Send the message as a broadcast, which will cause the server to forward it to all other users in the session.
            this.serverConnection.Broadcast(
                msg,
                MessagePriority.Immediate,
                MessageReliability.UnreliableSequenced,
                MessageChannel.Avatar);
        }
    }

    public void SendStageTransform(Vector3 position, Quaternion rotation)
    {
        // If we are connected to a session, broadcast our head info
        if (this.serverConnection != null && this.serverConnection.IsConnected())
        {
            // Create a tagged outgoing network message
            NetworkOutMessage msg = CreateMessage((byte)TestMessageID.StageTransform);
            // Attach the stage transform to the message
            AppendTransform(msg, position, rotation);
            // Log for debugging purposes
            UnityEngine.Debug.Log(getDateTime() + " Sent Stage Transform.");
            // Broadcast the message to the network
            BroadcastThisMessage(msg);
        }
    }

    public bool SendVector3(Vector3 v) {
        // If we are connected to a session, broadcast this vector
        if (this.serverConnection != null && this.serverConnection.IsConnected())
        {
            NetworkOutMessage msg = CreateMessage((byte)TestMessageID.ExperimentalVector3);
            AppendTimeStamp(msg);
            AppendVector3(msg, v);
            BroadcastThisMessage(msg);

            // Log this event
            // UnityEngine.Debug.Log(getDateTime() + " Sent experimental Vector3");
            return true;
        }
        else return false;
    }

    public bool SendInt(int myInt) {
        // If we're connected to a session, broadcast this integer
        if (this.serverConnection != null && this.serverConnection.IsConnected())
        {
            NetworkOutMessage msg = CreateMessage((byte)TestMessageID.ExperimentalInt);
            AppendTimeStamp(msg);
            msg.Write(myInt);
            BroadcastThisMessage(msg);

            // Log this event
            // UnityEngine.Debug.Log(getDateTime() + " Sent experimental integer");
            return true;
        }
        else {
            return false;
        }
    }

    public void BroadcastThisMessage(NetworkOutMessage msg) {
        // Send the message as a broadcast
        // This will cause the server to forward it to all other users in the session.
        this.serverConnection.Broadcast(
            msg,
            MessagePriority.Immediate,
            MessageReliability.ReliableOrdered,
            MessageChannel.Avatar);
    }

    void OnDestroy()
    {
        if (this.serverConnection != null)
        {
            for (byte index = (byte)TestMessageID.HeadTransform; index < (byte)TestMessageID.Max; index++)
            {
                this.serverConnection.RemoveListener(index, this.connectionAdapter);
            }
            this.connectionAdapter.MessageReceivedCallback -= OnMessageReceived;
        }
    }

    private int count = 0;
    void OnMessageReceived(NetworkConnection connection, NetworkInMessage msg)
    {
        byte messageType = msg.ReadByte();
        MessageCallback messageHandler = MessageHandlers[(TestMessageID)messageType];

        if (messageHandler != null)
        {
            // I don't understand how messageHandler isn't null for StageTransform... (1/2)
            UnityEngine.Debug.Log("Successfully read message handler : " + messageType.ToString());
            messageHandler(msg);
        }

        else
        {
            if (messageType.ToString() == "185")
            {
                // ExperimentalVector3

                count += 1;
                if (count % 1000 == 0)
                {
                    long senderID = msg.ReadInt64(); // Needed to be read first
                    double latency = ReadLatencyInMs(msg);
                    // UnityEngine.Debug.Log("Received a vector3 from " + msg.ReadInt64().ToString());
                    UnityEngine.Debug.Log("Vector3 Latency: " + latency.ToString());
                }
            }

            else if (messageType.ToString() == "186")
            {
                // ExperimentalInt
                count += 1;
                if (count % 1000 == 0) {
                    long senderID = msg.ReadInt64(); // Needed to be read first
                    double latency = ReadLatencyInMs(msg);
                    // UnityEngine.Debug.Log("Received an int from " + msg.ReadInt64().ToString());
                    UnityEngine.Debug.Log("Int Latency: " + latency.ToString());
                }
            }

        }
    }

    #region HelperFunctionsForWriting

    void AppendTransform(NetworkOutMessage msg, Vector3 position, Quaternion rotation)
    {
        AppendVector3(msg, position);
        AppendQuaternion(msg, rotation);
    }

    void AppendVector3(NetworkOutMessage msg, Vector3 vector)
    {
        msg.Write(vector.x);
        msg.Write(vector.y);
        msg.Write(vector.z);
    }

    void AppendQuaternion(NetworkOutMessage msg, Quaternion rotation)
    {
        msg.Write(rotation.x);
        msg.Write(rotation.y);
        msg.Write(rotation.z);
        msg.Write(rotation.w);
    }

    void AppendTimeStamp(NetworkOutMessage msg) {
        DateTime currentTime = System.DateTime.Now;
        long timeAsLong = currentTime.ToBinary();
        msg.Write(timeAsLong);
    }

    #endregion HelperFunctionsForWriting

    #region HelperFunctionsForReading

    public Vector3 ReadVector3(NetworkInMessage msg)
    {
        return new Vector3(msg.ReadFloat(), msg.ReadFloat(), msg.ReadFloat());
    }

    public Quaternion ReadQuaternion(NetworkInMessage msg)
    {
        return new Quaternion(msg.ReadFloat(), msg.ReadFloat(), msg.ReadFloat(), msg.ReadFloat());
    }

    public double ReadLatencyInMs(NetworkInMessage msg) {
        DateTime currentTimeStamp = DateTime.Now;
        DateTime msgTimeStamp = DateTime.FromBinary(msg.ReadInt64());
        // The time stamps are in 100-ns units. We need them in ms, thus x 100 and then / 1,000,000
        double latency = currentTimeStamp.Subtract(msgTimeStamp).TotalMilliseconds;
        // double latency = (currentTimeStamp - msgTimeStamp) * (1 / 10000);
        UnityEngine.Debug.Log(currentTimeStamp + " - " + msgTimeStamp + " = " + latency);
        return latency;
    }

    #endregion HelperFunctionsForReading

	// Helper method for getting time stamps as strings.
	// These time stamps will be attached to the output data files
	public string getDateTime() {
		return DateTime.Now.ToString() + " ";
	}
}