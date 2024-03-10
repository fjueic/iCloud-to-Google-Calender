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

    form.addParagraphTextItem().setTitle("Data");
  }
}


function setup(){
  createFiles();
}
