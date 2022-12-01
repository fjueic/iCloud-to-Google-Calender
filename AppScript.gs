var sheet = SpreadsheetApp.openById("");
var data =sheet.getDataRange().getValues();
data = data[data.length-1]
// Calendar to output requests
var calendar = CalendarApp.getCalendarById("");

function csvToArray(csv) {
  rows = csv.split("\n");

  return rows.map(function (row) {
    return row.split(",");
  });
};
// # index 0 = name
// # index 1 = date
// # index 2 = start
// # index 3 = end
// # index 4 = location
// # index 5 = description
// # index 6 = color
// # index 7 = mail??????
// # index 8 = crate or delete event
function test(){
  data = csvToArray(data[2]);
  Logger.log(data)
}

function createEvent() {
  for (var i = 0; i < data.length; i++) {
    // index 0 = Name of the Event
    // index 1 = Start Time of the Event
    // index 2 = End Time of the Event
    // index 3 = Location of the Event
    // index 4 = Description of the Event
    var Events = calendar.createEvent(data[i][0], new Date(`${data[i][1]} ${data[i][2]}`), new Date(`${data[i][1]} ${data[i][3]}`),
      { location: data[i][4], description: data[i][5] }).setColor(data[i][6]);
  }
}


function delete_events(fromDate, toDate) {
  var events = calendar.getEvents(fromDate, toDate);
  for (var i = 0; i < events.length; i++) {
    var ev = events[i];
    // show event name in log
    ev.deleteEvent();
  }
}
function temp (){
  delete_events(new Date("9/1/2021 5:00"),new Date("10/10/2023 5:00"))
}
var body = ""
function mail(action,date,start,end){
  if(action.trim()=="Create"){
    var status = "---ADDED"
  }else{
    var status = "---REMOVED"
  }
  var date = date.split("/")
  body = body + `${date[1]}/${date[0]}/${date[2]}   ${start}-${end} ${status}
  Check calender for details https://calendar.google.com/calendar/embed?src=${calendar.getId()}\n`
}
function send(){
  GmailApp.sendEmail(Session.getActiveUser().getEmail(), "Class updated", body);
}

function main(){
// for classes

  if(data[1]=="Classes"){
    data = csvToArray(data[2]);
    for(var i=0;i<data.length;i++){
      // send mail
      if(data[i][7]=="Mail"){




        if(data[i][8]=="Create"){
          // create event
          calendar.createEvent(data[i][0], new Date(`${data[i][1]} ${data[i][2]}`), new Date(`${data[i][1]} ${data[i][3]}`),
        {
          location: data[i][4],
          description: data[i][5]
        }).setColor(data[i][6]);
        mail(data[i][8],data[i][1],data[i][2],data[i][3]);
        }else{
          // delete event
          delete_events(new Date(`${data[i][1]} ${data[i][2]}`), new Date(`${data[i][1]} ${data[i][3]}`));
          mail(data[i][8],data[i][1],data[i][2],data[i][3]);
        }




      }else{
        // don't send mail
        calendar.createEvent(data[i][0], new Date(`${data[i][1]} ${data[i][2]}`), new Date(`${data[i][1]} ${data[i][3]}`),
        {
          location: data[i][4],
          description: data[i][5]
        }).setColor(data[i][6]);
    }
  }
  // updating attendence
  }else{
    data = csvToArray(data[2]);
    Logger.log(data);
    for(var i=0;i<data.length;i++){
      // get the calender event
      var events = calendar.getEvents(new Date(`${data[i][0]} ${data[i][1]}`),
      new Date(`${data[i][0]} ${data[i][2]}`));

      try{
        if(data[i][3]=="P"){
        // was present
        events[0].setColor("10");
        }else{
        // was absent
        events[0].setColor("11");
        }
      }catch(err){
        Logger.log("No class found")
      }

    }
  }
  send();
}

