using UnityEngine;
using UnityEngine.UI;
using System;
using System.Collections;
using System.IO.Ports;
using System.Threading;

/// <summary>
/// Handles bluetooth data.
/// Adapted from http://justkiel.com/wordpress/?p=1335.
/// </summary>
public class BluetoothClient : MonoBehaviour {

    // First activate the serial ports. Use Settings --> Devices --> 
    // Bluetooth & Other Devices --> More Bluetooth Options --> COM Ports

    private SerialPort serialPort = null;
    String portName = "COM3";   
    int baudRate = 115200;      
    int readTimeOut = 100;      
    int bufferSize = 32;    

    bool programActive = true;
    Thread thread;

    /// <summary>
    /// Initialize resources needed for the program.
    /// 1) Setup the bluetooth serial port and start the thread that handles msgs.
    /// </summary>
    void Start() {

        try {
            // Set the properties of the serial port.
            serialPort = new SerialPort();
            serialPort.PortName = portName;
            serialPort.BaudRate = baudRate; 
            serialPort.ReadTimeout = readTimeOut; 
            serialPort.Open();
            Debug.Log("Opened port " + serialPort.PortName);
        }
        catch (Exception e) {
            Debug.Log(e.Message);
        }

        // Execute a thread to manage the incoming BT data.
        // Don't read data in the update() method since reads block the program.
        thread = new Thread(ProcessData);
        thread.Start();
    }

    /// <summary>
    /// Process the incoming BT data on the virtual serial port.
    /// </summary>
    void ProcessData() {
        Byte[] buffer = new Byte[bufferSize];
        int bytesRead = 0;
        Debug.Log("Thread started");

        while (programActive) {
            try {
                // Attempt to read data from the BT device
                // - will throw an exception if no data is received within the timeout period
                bytesRead = serialPort.Read(buffer, 0, bufferSize);

                // Use the appropriate SerialPort read method for your BT device e.g. ReadLine(..) for newline terminated packets 

                if (bytesRead > 0)
                {
                    Debug.Log("Received data. Let me print it!");
                    Debug.Log(buffer);
                }
            }
            catch (TimeoutException)
            {
                // Do nothing, the loop will be reset
            }
        }
        Debug.Log("Thread stopped");
    }

    /// <summary>
    /// Update this instance.
    /// </summary>


    void Update()
    {
    }

    /// <summary>
    /// On program exit.
    /// </summary>


    public void OnDisable()
    {
        programActive = false;

        if (serialPort != null && serialPort.IsOpen)
            serialPort.Close();
    }
}
