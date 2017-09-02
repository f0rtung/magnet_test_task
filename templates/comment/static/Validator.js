function Validator(){

	this.validateNotEmptyValue = function(value){
		return 0 != value.length;
	}

	this.validateEmail = function(email){
		return /^[a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,}$/i.test(email);
	}

	this.validatePhone = function(phone){
		const phoneRE = new RegExp("^\\(\\d{3}\\)(\\d{7})");
		return null != phone.match(phoneRE);
	}
}