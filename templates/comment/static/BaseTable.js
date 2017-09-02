function BaseTable(tableID, tableTitles){
	self = this;
	this.tableID = tableID;
	this.tableTitles = tableTitles;
	this.createTableElement();
	this.createTableTitle();
	this.createTableRows();
	this.setClickEventDispatcher();
}

BaseTable.prototype.createTableElement = function(){
	tableObj = $("<table/>", { id: this.tableID, border: 1 });
	$("body").append(tableObj);
	this.table = tableObj;
}

BaseTable.prototype.createOneTableRow = function(createElementsCallback, values){
	const trEelem = $("<tr/>");
	trEelem.append(createElementsCallback(trEelem, values))
	return trEelem;
}

BaseTable.prototype.createTableColumns = function(parentTrElem, values){
	values.forEach(function(value){
		const tdElem = $("<td/>");
		thElem.text(value);
		parentTrElem.append(thElem);
	});
}

BaseTable.prototype.createTableTitleCallback = function(parentTrElem, values){
	values.forEach(function(value){
		const thElem = $("<th/>");
		thElem.text(value);
		parentTrElem.append(thElem);
	});
}

BaseTable.prototype.createTableRowCallback = function(parentTrElem, values){
	self.createTableColumns(parentTrElem, values);
}

BaseTable.prototype.createTableTitle = function(){
	const titleRow = this.createOneTableRow(this.createTableTitleCallback, this.tableTitles);
	this.table.append(titleRow);
}

BaseTable.prototype.getRowsData = function(callback){

}

BaseTable.prototype.createTableRows = function(){
	function createRowsCallback(rowsData){
		rowsData.forEach(function(rowData){
			const row = self.createOneTableRow(self.createTableRowCallback, rowData);
			self.table.append(row);
		});
	}
	this.getRowsData(createRowsCallback);
}

BaseTable.prototype.setClickEventDispatcher = function(){}