﻿using Academy.HoloToolkit.Sharing;
using Academy.HoloToolkit.Unity;
using System.Collections.Generic;
using System;
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
            Debug.Log(getDateTime() + " Sent Stage Transform.");
            // Broadcast the message to the network
            BroadcastThisMessage(msg);
        }
    }

    public void SendVector3(Vector3 v) {
        // If we are connected to a session, broadcast this vector
        if (this.serverConnection != null && this.serverConnection.IsConnected())
        {
            // Create an outgoing network message tagged as 'experimental data'
            NetworkOutMessage msg = CreateMessage((byte)TestMessageID.ExperimentalVector3);
            // Attach the vector to the message
            AppendVector3(msg, v);
            // Log this event
            Debug.Log(getDateTime() + " Sent experimental Vector3");
            // Broadcast this to the network
            BroadcastThisMessage(msg);
        }
    }

    public void SendInt(int myInt) {
        // If we're connected to a session, broadcast this integer
        if (this.serverConnection != null && this.serverConnection.IsConnected()) {
            // Create an outgoing message network tagged as 'experimental data'
            NetworkOutMessage msg = CreateMessage((byte)TestMessageID.ExperimentalInt);
            // Attach the integer to the message
            msg.Write(myInt);
            // Log this event
            Debug.Log(getDateTime() + " Sent experimental integer");
            // Broadcast this to the network
            BroadcastThisMessage(msg);
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

    void OnMessageReceived(NetworkConnection connection, NetworkInMessage msg)
    {
        byte messageType = msg.ReadByte();
        MessageCallback messageHandler = MessageHandlers[(TestMessageID)messageType];

        if (messageHandler != null)
        {
            // I don't understand how messageHandler isn't null for StageTransform... (1/2)
            print("Successfully read message handler : " + messageType.ToString());
            messageHandler(msg);
        }

        else {

            var hologramPlacementScript = GetComponent<HologramPlacement>();

            print("The message handler was actaully null for " + messageType.ToString() + " Type of script call: " + hologramPlacementScript.ToString());
            // ... Therefore, I'll do call the functions manually for my methods (2/2)

            if (messageType.ToString() == "185") {
                // ExperimentalVector3
                hologramPlacementScript.OnExperimentalVector3(msg);
            }

            else if (messageType.ToString() == "186") {
                // ExperimentalInt
                hologramPlacementScript.OnExperimentalInt(msg);
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
}