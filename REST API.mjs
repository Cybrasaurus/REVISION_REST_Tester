
import {json2xml} from "xml-js";

function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);
}

//httpGetAsync("http://127.0.0.1:5000/xml", "Return")

var json_data = [];

async function json_to_xml()
{

    const json = JSON.stringify(json_data)

    const xml = json2xml(json, { compact: true, spaces: 4 });

    console.log(xml);
}
async function HTTP_Request(theUrl)
{
    const res = await fetch(theUrl);
    if (res.ok) {
        json_data = await res.json();
        //const data = await res.body();
        console.log(json_data);
                }
    json_to_xml();
}


HTTP_Request("http://127.0.0.1:5000/json");

