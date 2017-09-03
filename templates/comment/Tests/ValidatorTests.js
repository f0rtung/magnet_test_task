describe("validateEmail", function(){
	const validator = new Validator();

	it("Check correct emails", function(){
		assert.isTrue(validator.validateEmail("vasya.zadov@gmail.com"));
		assert.isTrue(validator.validateEmail("vasya.zadov@mail.ru"));
		assert.isTrue(validator.validateEmail("vasya.zadov@yandex.ru"));
		assert.isTrue(validator.validateEmail("vasya@yandex.ru"));
	});

	it("Check incorrect emails", function(){
		assert.isFalse(validator.validateEmail("vasya.zadov@gmail"));
	});
});

describe("validatePhone", function(){
	const validator = new Validator();

	it("Check phone +7(111)222-33-11", function(){
		assert.isFalse(validator.validatePhone("+7(111)222-33-11"));
	});

	it("Check phone (111)222-33-119", function(){
		assert.isFalse(validator.validatePhone("(111)222-33-119"));
	});

	it("Check phone (111)22233-44", function(){
		assert.isFalse(validator.validatePhone("(111)22233-44"));
	});

	it("Check phone (222)4445566", function(){
		assert.isTrue(validator.validatePhone("(222)4445566"));
	});

	it("Check phone (222)444556-6", function(){
		assert.isFalse(validator.validatePhone("(222)444556-6"));
	});

	it("Check phone (222)44455667", function(){
		assert.isFalse(validator.validatePhone("(222)44455667"));
	});

	it("Check phone (222)444556", function(){
		assert.isFalse(validator.validatePhone("(222)444556"));
	});

	it("Check phone 2224445566", function(){
		assert.isFalse(validator.validatePhone("2224445566"));
	});
});