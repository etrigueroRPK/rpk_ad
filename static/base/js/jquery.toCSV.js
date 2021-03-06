jQuery.fn.toCSV = function() {
    var data = $(this).first(); //Only one table
    var csvData = [];
    var tmpArr = [];
    var tmpStr = '';
    data.find("tr").each(function() {
        var th=$(this).find("th");
        if(th.length) {
            th.each(function() {
              tmpStr = $(this).text().replace(/"/g, '""');
              tmpArr.push('"' + tmpStr + '"');
            });
            csvData.push(tmpArr);
        } else {
            tmpArr = [];
               $(this).find("td").each(function() {
                    if($(this).text().match(/^-{0,1}\d*\.{0,1}\d+$/)) {
                        tmpArr.push(parseFloat($(this).text()));
                    } else {
                        tmpStr = $(this).text().replace(/"/g, '""');
                        tmpArr.push('"' + tmpStr + '"');
                    }
               });
            csvData.push(tmpArr.join(','));
        }
    });
    var output = csvData.join('\n');
    var uri = 'data:text/csv;charset=utf-8,' + encodeURIComponent(output);
    var downloadLink = document.createElement("a");
    downloadLink.href = uri;
    downloadLink.download = document.title ? document.title.replace(/ /g, "_") + ".csv" : "data.csv";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  }