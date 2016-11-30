// Javscript calls to massage the elastic search results for d3

/* Get sections of a video viewed by any student, sorted by student
{ "size": 1,
  "query": {
    "constant_score": {
      "filter": {
        "and": [
          { "match": { "mpid": "f7b7d4f5-b52e-4d9a-abe7-2a0208f9a9fe" } },
          { "match": { "action.type": "HEARTBEAT" } },
          { "match": { "action.is_playing": true } },
          { "match": { "is_live": false } },
          { "range": { "action.inpoint": { "from": 1 } }
          } ]
      }
    }
  },
  "aggs": { "huid": { "terms": { "field": "huid", "size": 0 },
      "aggs": { "viewing": { "terms": { "field": "action.inpoint", "size": 0 } } } }
  } }
*/
// NOTE: An inpoint is produced every 30 seconds, each inpoint is roughly 1 min of viewing

// Sums up all the heartbeats to estimate amount of the video viewed
// assume format of results = 
//  js["aggregations"]["huid"]["buckets"][0]["viewing"]["buckets"]
function getStudentViewDuration(results) {
    if (results.hits.hits.length != 0) {
        return( +results.hits.hits[0]._source.episode.duration/1000); // from ms to s
    }
    return 0;
}

function tallyStudentView(results) {
    one = results.sort( function(a,b) { return a['key'] - b['key'];}); // ascending
    var viewed=0    // total
    var lastv = 0;
    var skipped=0;
    for (var j = 0; j < one.length; j++) {
        var bucket = one[j]
        inpoint = +bucket["key"]
        if (inpoint - lastv > 60) {  //  there is a gap between inpoints, more than 2x 30 seconds
            viewed = viewed +  60;   //  assume watched 60 seconds
        }
        else {
            viewed = viewed + inpoint - lastv;
        }
        lastv = inpoint;
    }
    return viewed;
}

// From the same data as above
// Produces an array of inpoints for each student
// Each inpoint = 1 min of video (-30 to +30)
function CollectStudentView(results) {
    var arr= new Array();
    one = results.sort( function(a,b) { return a['key'] - b['key'];}); // ascending
    for (var j = 0; j < one.length; j++) {
        arr.push(+one[j]["key"]);
    }
    return arr;
}


/* Get number of times each 5 min interval of one VOD is viewed by all students
{ "query": {
    "constant_score": {
      "filter": {
        "and": [
          { "match": { "mpid": "e20915d6-f314-4783-aac2-16e414dc32ef" } },
          { "match": { "action.type": "HEARTBEAT" } },
          { "match": { "action.is_playing": true } },
          { "match": { "is_live": 0 } }
        ] } }
  },
  "size": 0,
  "aggs": { "intervals": { "histogram": { "field": "action.inpoint", "interval": 300 },
      "aggs": { "users": { "terms": { "field": "huid" },
          "aggs": { "period": { "date_histogram": { "field": "@timestamp", "format": "yyyy-MM-dd HH:mm:ss", "interval": "1h", "min_doc_count": 1 } } } } } }
  }}
*/

// Based on the query above, but used bucket names from the django es.py module
// Flattens the data, works better than the d3.nested call
function tallyViewCount(data) {
  var inpoints = data.aggregations.by_inpoint.buckets;
  var nested=new Array();
  for (i = 0; i < inpoints.length; i++) {
    var inpoint= inpoints[i];
        // filter out negative inpoints - dirty data?
    if (inpoint.key > -1 & inpoint.by_user != null ) {
        var sum = 0
        var users = inpoint.by_user.buckets
        for (j = 0; j < users.length; j++) {
            var periods = users[j].by_period.buckets
            sum += periods.length;
        }
        nested.push({"key": inpoint.key, "values": sum }); 
    }
  }
  nested.sort(function (a, b) {
      if (a.key > b.key) {
        return 1;
      }
      if (a.key < b.key) {
        return -1;
      }
      return 0;
  });
  return nested;
}
