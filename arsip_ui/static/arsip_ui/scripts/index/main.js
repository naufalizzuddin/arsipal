document.getElementById('category-select').addEventListener('change', function() {
    const searchInput = document.getElementById('arsip-search-bar');
    const dateInputUntil = document.getElementById('date_until');
    const selectedValue = this.value;
    if (selectedValue === 'Tanggal Surat' || selectedValue === 'Tanggal Input') {
        searchInput.type = 'date';
        dateInputUntil.removeAttribute('hidden');
    } else {
        searchInput.type = 'text';
        searchInput.value = "";
        dateInputUntil.setAttribute('hidden', true);
    }

    searchInput.addEventListener('change', function (e){
        const dateValue = new Date(e.target.value);
        dateValue.setDate(dateValue.getDate() + 1);
        const newDateValue = dateValue.toISOString().split('T')[0];
        if (this.type === 'date') {
            dateInputUntil.value = newDateValue;
        }
    });
});

if (window.location.href.includes('/cari_dokumen/')) {
    const cancelSearchButton = document.getElementById('cancel-search');
    cancelSearchButton.classList.toggle('hidden');
}
  
document.addEventListener("DOMContentLoaded", function () {
    const sifatCells = document.querySelectorAll(".sifat-cell");
    const sifatColors = {
        "penting": "bg-red-500 text-white",
        "biasa": "bg-green-500 text-white",
        "segera": "bg-blue-500 text-white",
        "amat rahasia": "bg-fuchsia-700 text-white",
        "rahasia": "bg-purple-600 text-white",
        "khusus": "bg-yellow-500 text-white"
    };
    sifatCells.forEach((cell) => {
        const sifatValue = cell.textContent.trim().toLowerCase();
        const colorClass = sifatColors[sifatValue] || "bg-gray-500 text-white";
        cell.classList.add(...colorClass.split(" "));
    });

    document.getElementById('category-select').selectedIndex = 0;

    const exportButton = document.getElementById("export-button");
    const dropdownMenu = document.getElementById("dropdown-export");

    exportButton.addEventListener("click", function () {
        dropdownMenu.classList.toggle("hidden");
    });

    document.addEventListener("click", function (event) {
        if (!exportButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.add("hidden");
        }
    });
});
  
function getTableData() {
    const table = document.querySelector('table');
    const headers = [];
    const rows = [];

    const thElements = table.querySelectorAll('thead tr th');
    for(let i=0; i<6; i++) {
        headers.push(thElements[i].innerText.trim());
    }

    const trElements = table.querySelectorAll('tbody tr');
    trElements.forEach(tr => {
        const tdElements = tr.querySelectorAll('td');
        const row = [];
        for(let i=0; i<6; i++) {
            row.push(tdElements[i].innerText.trim());
        }
        rows.push(row);
    });

    return { headers, rows };
}

function generateCSVContent(headers, rows) {
    const csvRows = [];
    
    const escapedHeaders = headers.map(header => 
        header.includes(',') ? `"${header}"` : header
    );
    csvRows.push(escapedHeaders.join(','));
    
    rows.forEach(row => {
        const escapedRow = row.map(cell => 
            cell.includes(',') ? `"${cell}"` : cell
        );
        csvRows.push(escapedRow.join(','));
    });
    
    return csvRows.join('\r\n');
}

function exportToCSV() {
    const { headers, rows } = getTableData();
    const csvContent = generateCSVContent(headers, rows);
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.href = url;
    link.setAttribute('download', 'dokumen.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

function exportToExcel() {
    const { headers, rows } = getTableData();

    // Function to calculate the maximum width of text in a column
    function calculateColumnWidth(data) {
        let maxWidth = 0;
        data.forEach(cell => {
            const cellWidth = cell ? cell.toString().length : 0;
            if (cellWidth > maxWidth) {
                maxWidth = cellWidth;
            }
        });
        return maxWidth;
    }

    // Calculate the maximum width for each column
    const columnWidths = headers.map((header, colIndex) => {
        const columnData = [header, ...rows.map(row => row[colIndex])];
        return calculateColumnWidth(columnData);
    });

    // Create the XML structure for the Excel file
    const xml = `
        <?xml version="1.0"?>
        <Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
                  xmlns:o="urn:schemas-microsoft-com:office:office"
                  xmlns:x="urn:schemas-microsoft-com:office:excel"
                  xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
                  xmlns:html="http://www.w3.org/TR/REC-html40">
            <Styles>
                <!-- Define a style for bold text -->
                <Style ss:ID="boldHeader">
                    <Font ss:Bold="1"/>
                </Style>
                <!-- Define a style for text wrapping -->
                <Style ss:ID="wrapText">
                    <Alignment ss:WrapText="1"/>
                </Style>
            </Styles>
            <Worksheet ss:Name="Sheet1">
                <Table>
                    ${columnWidths.map(width => `<Column ss:Width="${width + 110}"/>`).join('')}
                    <Row>
                        ${headers.map(header => `<Cell ss:StyleID="boldHeader"><Data ss:Type="String">${header}</Data></Cell>`).join('')}
                    </Row>
                    ${rows.map(row => `
                        <Row>
                            ${row.map(cell => `<Cell ss:StyleID="wrapText"><Data ss:Type="String">${cell}</Data></Cell>`).join('')}
                        </Row>
                    `).join('')}
                </Table>
            </Worksheet>
        </Workbook>
    `;

    // Create a Blob with the XML content
    const blob = new Blob([xml], { type: 'application/vnd.ms-excel' });

    // Create a download link and trigger the download
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.setAttribute('download', 'dokumen.xls');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('export-csv').addEventListener('click', exportToCSV);
    document.getElementById('export-excel').addEventListener('click', exportToExcel);
});
