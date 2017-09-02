function AllCommentsTable(){
	const tableTitles = [
		"Фамилия",
		"Имя",
		"Отчество",
		"Регион",
		"Город",
		"Электронная почта",
		"Телефон",
		"Комментарий",
		"Действие"
	]
	BaseTable.call(this, "allCommentsTableID", tableTitles);
}

AllCommentsTable.prototype = Object.create(BaseTable.prototype);
AllCommentsTable.prototype.constructor = AllCommentsTable;

AllCommentsTable.prototype.getRowsData = function(callback){
	ajaxQuery("/api/get_all_comments", {}, "post", function(response){
		callback(response);
	});
}

AllCommentsTable.prototype.createTableColumns = function(parentTrElem, rowValues){
	rowValues.forEach(function(value, index, values){
		const tdElem = $("<td/>");
		if(index == values.length - 1){
			const refEelem = $("<a/>", {href: "", commentID: value});
			refEelem.text("Удалить");
			tdElem.append(refEelem);
		}
		else{
			tdElem.text(value);
		}
		parentTrElem.append(tdElem);
	});
}

AllCommentsTable.prototype.setClickEventDispatcher = function(){
	function redrawComments(){
			self.table.empty();
			self.createTableTitle();
			self.createTableRows();
		}

	function removeComment(commentID){
		ajaxQuery("/api/remove_comment_by_id", {commentID: commentID}, 
				  "post", function(response){
				redrawComments();
			});
	}

	self.table.click(function(event){
		const target = event.target;
		if(target.tagName == "A"){
			event.preventDefault();
			const commentID = $(target).attr("commentID");
			removeComment(commentID);
		}
	});
}