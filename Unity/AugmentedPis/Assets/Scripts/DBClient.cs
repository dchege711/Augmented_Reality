using System;
using UnityEngine;
using MongoDB.Driver;
using MongoDB.Bson;

// Current MongoDB won't work for Unity. I'm using v1.11.0 from this guy:
// http://answers.unity3d.com/questions/618708/unity-and-mongodb-saas.html
// Remember to set the Unity API Compatibility Level as ".NET 2.0" rather than ".NET 2.0 Subset"

// The syntax for v1.11.0 differs considerably from the current v2.4.4

public class DBClient : MonoBehaviour {
    void Start() {
        string uri = "mongodb://ar-projects:sCQWaRWCzoS01RbIUNAL05dj0VlO9acJficROoIywMwm3DYRexg4e1J6IZwJmuJVvrVpfhD05QaCPWcsRlptjw==@ar-projects.documents.azure.com:10255/?ssl=true&replicaSet=globaldb";
        // string uri = "mongodb://localhost";

        MongoClient client = new MongoClient(new MongoUrl(uri));

        var server = client.GetServer();
        server.Connect();
        var db = server.GetDatabase("Test");
        MongoCollection<BsonDocument> collection = db.GetCollection<BsonDocument>("testCol");
        BsonDocument document = new BsonDocument {
            { "testX", "This is test #2." },
            { "testY", "I hope it makes it to Azure..." }
        };
        collection.Insert(document);

        // Query the database
        var query = MongoDB.Driver.Builders.Query.EQ("testX", "This is a test.");
        var fetchedDocs = collection.Find(query);
        foreach (BsonDocument doc in fetchedDocs) {
            Console.WriteLine(doc);
        }
        
    }
}
