using Academy.HoloToolkit.Sharing;
using Academy.HoloToolkit.Unity;
using System.Collections.Generic;
using System;
using UnityEngine;

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

	/// <summary>
	/// Chege: Helper variables for logging data
	/// </summary>
	string filePathIncoming = @"C:\Users\dchege711\Documents\Augmented_Reality\Unity\SharingBasics\Data_Dumps\Incoming.txt";
	string filePathOutgoing = @"C:\Users\dchege711\Documents\Augmented_Reality\Unity\SharingBasics\Data_Dumps\Outgoing.txt";

    void Start()
    {
        InitializeMessageHandlers();

		// Open text files for logging the messages sent
		// System.IO.File.WriteAllText(filePathIncoming, getDateTime());
		// System.IO.File.WriteAllText(filePathOutgoing, getDateTime());

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
        // Add the local userID so that the remote clients know whose message they are receiving
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

			// Chege: Log this message to a text file so that we see what's being sent
			// We'll be appending data to the text file instead of overwriting
			logMsgToTextFile(filePathOutgoing, getDateTime());
			logMsgToTextFile(filePathOutgoing, position.ToString());
			logMsgToTextFile(filePathOutgoing, rotation.ToString());
			logMsgToTextFile(filePathOutgoing, msg.ToString());

            // Try setting a variable that will be accessed by SharingStage.cs
            string messageAsString = getDateTime() + " " + position.ToString() + " " + rotation.ToString();
            this.serverConnection.recordMessage(messageAsString);

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
            // Create an outgoing network message to contain all the info we want to send
            NetworkOutMessage msg = CreateMessage((byte)TestMessageID.StageTransform);

            AppendTransform(msg, position, rotation);

			// Chege: Log this message to a text file so that we see what's being sent
			// We'll be appending data to the text file instead of overwriting
			logMsgToTextFile(filePathOutgoing, getDateTime());
			logMsgToTextFile(filePathOutgoing, position.ToString());
			logMsgToTextFile(filePathOutgoing, rotation.ToString());

            // Try setting a variable that will be accessed by SharingStage.cs
            string messageAsString = getDateTime() + " " + position.ToString() + " " + rotation.ToString();
            this.serverConnection.recordMessage(messageAsString);

            logMsgToTextFile(filePathOutgoing, msg.ToString());

            // Send the message as a broadcast, which will cause the server to forward it to all other users in the session.
            this.serverConnection.Broadcast(
                msg,
                MessagePriority.Immediate,
                MessageReliability.ReliableOrdered,
                MessageChannel.Avatar);
        }
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

    void OnMessageReceived(NetworkConnection connection, NetworkInMessage msg)
    {
        byte messageType = msg.ReadByte();
        MessageCallback messageHandler = MessageHandlers[(TestMessageID)messageType];

		// Chege: Log this message to a text file so that we see what's being received
		// We'll be appending data to the text file instead of overwriting
		logMsgToTextFile(filePathIncoming, getDateTime());
		// Apparently, we're not supposed to mess with NetworkInMessage w/o parental guidance
		// Let's see if we can get a string representation 
		logMsgToTextFile(filePathIncoming, msg.ReadString().ToString());
		// And also the size of the message
		logMsgToTextFile(filePathIncoming, msg.ToString());

        if (messageHandler != null)
        {
            messageHandler(msg);
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

	// Added by Chege
	void logMsgToTextFile(string filePath, string message) 
	{
		using (System.IO.StreamWriter file = 
			new System.IO.StreamWriter(filePath, true))
		{
			file.WriteLine(message);
		}
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

    #endregion HelperFunctionsForReading

	// Helper method for getting time stamps as strings.
	// These time stamps will be attached to the output data files
	public string getDateTime() {
		return DateTime.Now.ToString() + " ";
	}

	// Helper method for converting bytes to strings
	public string convertByteToString(byte myByte) {
		return System.Text.Encoding.ASCII.GetString (new[] {myByte});
	}
}