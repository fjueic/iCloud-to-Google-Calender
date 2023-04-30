function createFiles() {
  const folderName = "iCloud-config";
  const sheetName = "iCloud-data";
  const formName = "iCloud-form";

  // Check if the iCloud-config folder exists in Google Drive, if not create it
  const folderIterator = DriveApp.getFoldersByName(folderName);
  let folder = null;
  if (folderIterator.hasNext()) {
    folder = folderIterator.next();
  } else {
    folder = DriveApp.createFolder(folderName);
  }

  // Check if the iCloud-data sheet exists in Google Drive, if not create it
  let sheet = null;
  const spreadsheetFiles = DriveApp.getFilesByType(MimeType.GOOGLE_SHEETS);
  while (spreadsheetFiles.hasNext()) {
    const spreadsheetFile = spreadsheetFiles.next();
    const spreadsheet = SpreadsheetApp.openById(spreadsheetFile.getId());
    if (spreadsheet.getName() === sheetName) {
      sheet = spreadsheet;
      break;
    }
  }
  if (!sheet) {
    sheet = SpreadsheetApp.create(sheetName);
    const sheetId = sheet.getId();
    const sheetFile = DriveApp.getFileById(sheetId);
    folder.addFile(sheetFile);
    DriveApp.getRootFolder().removeFile(sheetFile);
  }

  // Check if the iCloud-form form exists in Google Drive, if not create it
  let form = null;
  const formFiles = DriveApp.getFilesByType(MimeType.GOOGLE_FORMS);
  while (formFiles.hasNext()) {
    const formFile = formFiles.next();
    const currentForm = FormApp.openById(formFile.getId()).getTitle();
    if (currentForm === formName) {
      form = FormApp.openById(formFile.getId());
      break;
    }
  }
  if (!form) {
    form = FormApp.create(formName);
    const formId = form.getId();
    const formFile = DriveApp.getFileById(formId);
    folder.addFile(formFile);
    DriveApp.getRootFolder().removeFile(formFile);

    // Add form questions
    const formItem = form.addMultipleChoiceItem();
    formItem.setTitle("Type");
    formItem.setChoices([
      formItem.createChoice("Classes"),
      formItem.createChoice("Attendance")
    ]);
    form.addParagraphTextItem().setTitle("Data");
  }
}




function getSheetIdAndFormUrl() {
  // Get the folder named "iCloud-config"
  data = {};
  const folderName = "iCloud-config";
  const folders = DriveApp.getFoldersByName(folderName);
  if (folders.hasNext()) {
    const folder = folders.next();
    
    // Get the sheet named "iCloud-data" in the "iCloud-config" folder
    const sheetName = "iCloud-data";
    const sheets = folder.getFilesByName(sheetName);
    if (sheets.hasNext()) {
      const sheet = sheets.next();
      const sheetId = sheet.getId();
      Logger.log("Sheet ID: " + sheetId);
      data["id"]=sheetId;
    } else {
      Logger.log("Sheet not found!");
    }
    
    // Get the form named "iCloud-form" in the "iCloud-config" folder
    const formName = "iCloud-form";
    const forms = folder.getFilesByName(formName);
    if (forms.hasNext()) {
      const form = forms.next();
      const formUrl = form.getUrl();
      Logger.log("Form URL: " + formUrl);
      data["form-url"]=formUrl;
    } else {
      Logger.log("Form not found!");
    }
  } else {
    Logger.log("Folder not found!");
  }
  var jsonString = JSON.stringify(data);
  
  // get folder by name "iCloud-config"
  var folder = DriveApp.getFoldersByName("iCloud-config").next();
  
  // create file in the folder with name "data.json"
  var file = folder.createFile("data.json", jsonString, MimeType.PLAIN_TEXT);
}

function setup(){
  createFiles();
  getSheetIdAndFormUrl();
}

