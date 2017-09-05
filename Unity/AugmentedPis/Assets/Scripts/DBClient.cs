using System;
using UnityEngine;
using MongoDB.Driver;
using MongoDB.Bson;

// Current MongoDB won't work for Unity. I'm using v1.11.0 from this guy:
// http://answers.unity3d.com/questions/618708/unity-and-mongodb-saas.html
// Remember to set the Unity API Compatibility Level as ".NET 2.0" rather than ".NET 2.0 Subset"

// The syntax for v1.11.0 differs considerably from the current v2.4.4

/// <summary>
/// Handles connections, reads and writes to MongoDB.
/// Currently buggy: Complains of an ssl connection.
/// </summary>
public class DBClient : MonoBehaviour {

    // Declare variables that need to be accessed by different methods.
    MongoServer server;

    void Start() {
        string uri = "mongodb://ar-projects:sCQWaRWCzoS01RbIUNAL05dj0VlO9acJficROoIywMwm3DYRexg4e1J6IZwJmuJVvrVpfhD05QaCPWcsRlptjw==@ar-projects.documents.azure.com:10255/?ssl=true";
        // string uri = "mongodb://localhost";

        MongoClient client = new MongoClient(new MongoUrl(uri));
        server = client.GetServer();
        server.Connect();  
    }

    void TestRun() {
        var db = server.GetDatabase("Test");
        var collection = db.GetCollection<BsonDocument>("testCol");
        BsonDocument document = new BsonDocument {
            { "testX", "This is test #3." },
            { "testY", "I hope it makes it to Azure..." }
        };
        var result = InsertDoc(collection, document);
        Debug.Log(result);
    }

    /// <summary>
    /// Find the documents on a collection that match a key-value combination.
    /// </summary>
    /// <param name="collection">A MongoCollection object containing Bson Documents.</param>
    /// <param name="key">A string representing the field in the document.</param>
    /// <param name="value">The value that should be found at the key's location.</param>
    /// <returns> A MongoCursor that can be used to iterate through matching documents.</returns>
    MongoCursor QueryCollection(MongoCollection<BsonDocument> collection, string key, string value) {
        var query = MongoDB.Driver.Builders.Query.EQ(key, value);
        MongoCursor fetchedDocs = collection.Find(query);
        return fetchedDocs;
    }

    /// <summary>
    /// Insert a BsonDocument into the specified collection.
    /// </summary>
    /// <param name="collection">A MongoCollection object containing Bson Documents.</param>
    /// <param name="doc">The Bson Document that needs to be added to the database.</param>
    /// <returns>A WriteConcernResult that contains information about the write.</returns>
    WriteConcernResult InsertDoc(MongoCollection<BsonDocument> collection, BsonDocument doc) {
        return collection.Insert(doc);
    }
}
