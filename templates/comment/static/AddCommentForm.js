function AddCommentForm(){
	const self = this;
	const formID = "addCommentForm";
	const submitBtnID = "submitButton";
	const inputErrorClassName = "error";
	const validator = new Validator();

	function prepareInvalidInputs(inputNames){
		inputNames.forEach(function(name){
			const elem = $("[name=\"" + name + "\"]", self.form);
			elem.addClass(inputErrorClassName);
		});
	}

	function selectInitialization(thisElement, apiUrl, queryData){
		const callBack = function(response){
			response.forEach(function(region){
				const id = region[0];
				const value = region[1];
				const newOptionElement = $("<option/>", {value: id});
				newOptionElement.text(value)
				thisElement.append(newOptionElement);
			})
		}
		ajaxQuery(apiUrl, queryData, "POST", callBack, false);
	}

	function regionsInitialization(thisElement){
		selectInitialization(thisElement, "/api/get_all_regions", {});
	}

	function citiesInitialization(thisElement, regionID){
		selectInitialization(thisElement, 
							 "/api/get_all_cities_by_reg_id", 
							 {regionID: regionID});
	}

	self.formElements = {
		"fName": {
		    tag: "<input/>",
			tagOption: {
				type: "text",
				name: "fName",
				placeholder: "First name"
			},
			validate: function(fName){
				return validator.validateNotEmptyValue(fName);
			}
		},
		"sName": {
		    tag: "<input/>",
			tagOption: {
				type: "text",
				name: "sName",
				placeholder: "Second name"
			},
			validate: function(sName){
				return validator.validateNotEmptyValue(sName);
			}
		},
		"mName": {
		    tag: "<input/>",
			tagOption: {
				type: "text",
				name: "mName",
				placeholder: "Middle name"
			}
		},
		"region": {
		    tag: "<select/>",
			tagOption: {
				name: "region",
				change: function(){
					const citySelect = $("[name=city]", self.form);
					citySelect.empty();
					citiesInitialization(citySelect, this.value);
				}
			},
			initialization: regionsInitialization
		},
		"city": {
		    tag: "<select/>",
			tagOption: {
				name: "city"
			},
			initialization: function(thisElement){
				const regID = $("[name=region]", self.form)[0].value;
				citiesInitialization(thisElement, regID);
			}
		},
		"email": {
		    tag: "<input/>",
			tagOption: {
				type: "text",
				name: "email",
				placeholder: "E-mail"
			},
			validate: function(email) {
				return validator.validateEmail(email);
			}
		},
		"phone": {
		    tag: "<input/>",
			tagOption: {
				type: "text",
				name: "phone",
				placeholder: "Phone"
			},
			validate: function(phone) {
				return validator.validatePhone(phone);
			}
		},
		"comment": {
		    tag: "<textarea/>",
			tagOption: {
				type: "text",
				name: "comment",
				placeholder: "Comment"
			},
			validate: function(comment) {
				return validator.validateNotEmptyValue(comment);
			}
		},
		"submitBtn": {
		    tag: "<input/>",
			tagOption: {
				type: "submit",
				id: submitBtnID,
				click: function(event){
					event.preventDefault();
					self.submit();
				}
			}
		}
	}

	function createForm(elemnts){
		formObj = $("<form/>", {
			id: formID,
			method: "post",
			action: "/api/add_comment"
		});
		$("body").append(formObj);
		self.form = formObj;
		for(elemIdx in elemnts){
			const element = elemnts[elemIdx];
			appEndElement(formObj, element.tag, element.tagOption, element.initialization);
		}
	}

	function appEndElement(formObj, elementTag, elementOptions, elementInitFunc){
		const pTag = $("<p/>");
		const newElement = $(elementTag, elementOptions)
		pTag.append(newElement);
		if(elementInitFunc != null)
		{
			elementInitFunc(newElement)
		}
		formObj.append(pTag);
	}

	self.getData = function(){
		const dataArr = self.form.serializeArray();
		const data = {}
		for(let idx = 0; idx < dataArr.length; ++idx){
			const name = dataArr[idx].name;
			const value = dataArr[idx].value;
			data[name] = value;
		}
		return data;
	}

	self.validate = function(){
		const validateResult = { isValid: true, errorFields: [] };
		const inputs = self.getData();
		for(name in inputs){
			const value = inputs[name];
			const validateFunc = self.formElements[name].validate
			if(validateFunc != null &&
			   !self.formElements[name].validate(value))
			{
				validateResult.isValid = false;
				validateResult.errorFields.push(name);
			}
		}
		return validateResult;
	}
	
	self.submit = function(){
		const validateResult = self.validate();
		$("[name]", self.form).removeClass(inputErrorClassName);
		if(!validateResult.isValid){
			prepareInvalidInputs(validateResult.errorFields);
		}
		else{
			ajaxQuery(self.form.attr("action"),
			          self.getData(),
			          self.form.attr("method"),
			          function(response){});
		}
	}

	createForm(self.formElements);
}