function csvToArray(csv) {
  let rows = csv.split("\n");
  return rows.map(function (row) {
    return row.split(",");
  });
}

function delete_events(calendar, fromDate, toDate) {
  var events = calendar.getEvents(fromDate, toDate);
  for (var i = 0; i < events.length; i++) {
    var ev = events[i];
    // show event name in log
    ev.deleteEvent();
  }
}

function del() {
  var calendar = CalendarApp.getDefaultCalendar();
  var events = calendar.getEvents(
    new Date("9/1/2021 5:00"),
    new Date("10/10/2024 5:00"),
  );
  Logger.log(events);
  Logger.log(events.length);
  for (var i = 0; i < events.length; i++) {
    var ev = events[i];
    // show event name in log
    ev.deleteEvent();
  }
}

function readSheet() {
  var sheetId = "SHEET_ID";
  var sheet = SpreadsheetApp.openById(sheetId).getActiveSheet();
  var calendar = CalendarApp.getDefaultCalendar();
  var data = sheet.getDataRange().getValues();
  data = data[data.length - 1][1];
  data = csvToArray(data);
  // 0: course_code 1: course_name 2: teacher 3: division 4: date 5: lectType 6: fromTime 7: toTime 8: day 9: roomno 10: batch_name 11: action 12: alternate

  for (let i = 0; i < data.length; i++) {
    var event = data[i];
    let date = event[4].trim().split("/");
    date = `${date[1]}/${date[2]}/${date[0]}`;
    if (event[11].trim() == "Removed" || event[11].trim() == "Changed") {
      delete_events(
        calendar,
        new Date(date + " " + event[6]),
        new Date(date + " " + event[7]),
      );
    }
    if (event[11].trim() == "Added" || event[11].trim() == "Changed") {
      calendar
        .createEvent(
          event[1] + " - " + event[0],
          new Date(date + " " + event[6]),
          new Date(date + " " + event[7]),
          {
            location: event[9],
            description: `Teacher: ${event[2]}\nDivision: ${event[3]}\nLecture Type: ${event[5]}\nBatch: ${event[10]}`,
          },
        )
        .setColor(
          event[12].trim() == "True"
            ? "3"
            : event[5].trim() == "PP"
              ? "4"
              : "7",
        );
    }
  }
}
