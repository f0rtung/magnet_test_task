function StatTable(){
	const tableTitles = [
		"Имя региона",
		"Количество комментариев регионе"
	]
	BaseTable.call(this, "statTableID", tableTitles);
}

StatTable.prototype = Object.create(BaseTable.prototype);
StatTable.prototype.constructor = StatTable;

StatTable.prototype.getRowsData = function(callback){
	ajaxQuery("/api/get_regions_stat", {}, "post", function(response){
		callback(response);
	});
}

StatTable.prototype.createTableColumns = function(parentTrElem, rowValues){
	const regionID = rowValues[0];
	const regionName = rowValues[1];
	const regionCommCount = rowValues[2];

	const tdRegNameElem = $("<td/>");
	const refEelem = $("<a/>", {href: "", regionID: regionID});
	refEelem.text(regionName);
	tdRegNameElem.append(refEelem);
	parentTrElem.append(tdRegNameElem);
	const tdRegCommCountElem = $("<td/>");
	tdRegCommCountElem.text(regionCommCount);
	parentTrElem.append(tdRegCommCountElem);
}

BaseTable.prototype.setClickEventDispatcher = function(){
	function showCitiesStat(regionID, parentElem){
		ajaxQuery("/api/get_cities_stat", {regionID: regionID}, 
				  "post", function(response){
				const ulElem = $("<ul/>", {type: "circle"});
				for(id in response){
					const cityName = response[id][0];
					const commCount = response[id][1];
					const liElem = $("<li/>");
					liElem.text(cityName + ": " + commCount);
					ulElem.append(liElem);
				}
				parentElem.append(ulElem);
			});
		}

	this.table.click(function(event){
		if(event.target.tagName == "A"){
			event.preventDefault();
			const aElem = $(event.target);
			const regionID = aElem.attr("regionID");
			const parentElem = aElem.parent();
			if(parentElem.has("ul").length){
				$("ul", parentElem).remove();
			}
			else{
				showCitiesStat(regionID, parentElem);
			}
		}
	});
}