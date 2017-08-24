using UnityEngine;
using UnityEngine.UI;
using System;
using System.Collections;
using System.IO.Ports;
using System.Threading;

public class BluetoothManager : MonoBehaviour {

    private SerialPort serialPort = null;
    // Possible strings include...
    public String portName = "COM1";
     // The maximum number of symbols (and in this case, bits) per second that
     // can be transferred
    public int baudRate =  115200;
    // The number of milliseconds before a read operation times out. Infinite by default
    public int readTimeOut = 100;
    // Useful for reading incoming packets
    public int numBytesToRead = 32;

    bool programActive = true;
    Thread thread;

    /// <summary>
    /// Setup the virtual port connection for the BT device at program start.
    /// </summary>
    void Start () {

        try
        {
            serialPort = new SerialPort();

            // Print the available ports
            string[] ports = serialPort.GetPortNames();
            foreach(string port in ports) {
                Debug.Log("Available Port: {0}", port);
            }

            // Set the attributes of the serialPort
            serialPort.PortName = portName;
            serialPort.BaudRate = baudRate;
            serialPort.ReadTimeout = readTimeOut;

            // Open the serialPort for incoming communication
            serialPort.Open();
        }
        catch (Exception e) {
            Debug.Log(e.Message);
        }

        // Execute a thread to manage the incoming BT data
        thread = new Thread(new ThreadStart(ProcessData));
        thread.Start();
    }

    /// <summary>
    /// Processes the incoming BT data on the virtual serial port.
    /// </summary>
    void ProcessData(){
        Byte[] buffer = new Byte[bufferSize];
        int bytesRead = 0;
        Debug.Log("Thread started");

        while(programActive) {
            // Attempt to read data from the BT device
            try {
                // Use the appropriate SerialPort read method for your BT device
                // e.g. ReadLine(..) for newline terminated packets

                // Throws an exception if no data is received within the timeout period
                // Writes the input to the Byte[] array (buffer) at offset 0.
                bytesRead = serialPort.Read(buffer, 0, numBytesToRead);

                if(bytesRead > 0){
                    // Do something with the data in the buffer
                }
            }

            catch(TimeoutException) {
                // Do nothing, the loop will be reset
            }
        }
        Debug.Log ("Thread stopped");
    }

    /// <summary>
    /// Update this instance.
    /// </summary>
    void Update () {
    }

    /// <summary>
    /// On program exit.
    /// </summary>
    public void OnDisable(){
        programActive = false;

        if (serialPort != null && serialPort.IsOpen)
            serialPort.Close ();
    }
}
