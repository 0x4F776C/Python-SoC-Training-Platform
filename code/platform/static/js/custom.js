function load() {
	var path = window.location.pathname;
	$("li#navlink a[href='" + path + "']").parent().addClass("active");
	$('[data-toggle="tooltip"]').tooltip();
}