let xlsx = require('xlsx');

let workbook = xlsx.readFile('./test.xlsx');
let sheet_name_list = workbook.SheetNames;

console.log(xlsx.utils.sheet_to_json(workbook.Sheets[sheet_name_list[0]]))