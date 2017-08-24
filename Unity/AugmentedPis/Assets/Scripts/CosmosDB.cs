using System;
using System.Linq;
using System.Threading.Tasks;

// ADD THIS PART TO YOUR CODE
using System.Net;
using Microsoft.Azure.Documents;
using Microsoft.Azure.Documents.Client;
using Newtonsoft.Json;

public class CosmosDB {

    // Get these constants from the Azure Portal
    private const string EndpointUrl = "<your endpoint URL>";
    private const string PrimaryKey = "<your primary key>";
    private DocumentClient client;

    static void Main(string[] args) {

        try {
            HelloCosmosDB p = new HelloCosmosDB();
            p.GetStartedDemo().Wait();
        }

        catch (DocumentClientException de) {
            Exception baseException = de.GetBaseException();
            Console.WriteLine("{0} error occurred: {1}, Message: {2}", de.StatusCode, de.Message, baseException.Message);
        }

        catch (Exception e) {
            Exception baseException = e.GetBaseException();
            Console.WriteLine("Error: {0}, Message: {1}", e.Message, baseException.Message);
        }

        finally {
            Console.WriteLine("End of demo, press any key to exit.");
            Console.ReadKey();
        }
    }

    private async Task Initialize() {
        this.client = new DocumentClient(new Uri(EndpointUrl), PrimaryKey);
    }

}
