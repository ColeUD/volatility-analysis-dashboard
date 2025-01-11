function uploadMetricsToSheet() {
  const fileId = "13slCqkAtkf9qOyBpiKJbeLBbV8CXThtyGPEjC3u8Z_4"; // Replace with your Google Sheet ID
  const sheetName = "Metrics";
  const csvUrl = "https://drive.google.com/uc?id=1DPrSmBve6eIJX9JNKZXed6zn43d30ECh&export=download"; // Replace with your direct download link

  try {
    // Fetch the CSV content
    const response = UrlFetchApp.fetch(csvUrl);
    const csvContent = response.getContentText();
    Logger.log("CSV content fetched successfully.");

    // Parse the CSV content
    const rows = Utilities.parseCsv(csvContent);
    Logger.log(`Parsed CSV. Number of rows: ${rows.length}, columns: ${rows[0].length}`);

    // Open the Google Sheet
    const spreadsheet = SpreadsheetApp.openById(fileId);
    Logger.log(`Opened spreadsheet: ${spreadsheet.getName()}`);

    // Access or create the target sheet
    let sheet = spreadsheet.getSheetByName(sheetName);
    if (!sheet) {
      Logger.log(`Sheet "${sheetName}" not found. Creating a new sheet.`);
      sheet = spreadsheet.insertSheet(sheetName);
    } else {
      Logger.log(`Using existing sheet: ${sheet.getName()}`);
    }

    // Clear the sheet
    sheet.clear();
    Logger.log(`Sheet cleared: ${sheetName}`);

    // Write data in batches
    const batchSize = 1000;
    for (let i = 0; i < rows.length; i += batchSize) {
      const chunk = rows.slice(i, i + batchSize);
      sheet.getRange(i + 1, 1, chunk.length, chunk[0].length).setValues(chunk);
      Logger.log(`Written batch ${i + 1} to ${i + chunk.length}`);
    }

    Logger.log("Data written successfully.");
  } catch (error) {
    Logger.log(`Error occurred: ${error.message}`);
  }
}
