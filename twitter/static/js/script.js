jQuery(document).on('click', '.btn-delete', function(){
	return confirm("Are you sure you want to delete this post?");
});

jQuery(document).on("input", "textarea", function(){
    var len = jQuery(this).val().length;
    var max = jQuery(this).attr("maxlength");
    jQuery(".count").text("Remaining: " + (max-len));
});

jQuery(document).ready(function(){
    var len = jQuery("textarea").val().length;
    var max = jQuery("textarea").attr("maxlength");
    jQuery(".count").text("Remaining: " + (max-len));
});

jQuery(document).on("input", ".create-post textarea", function(){
    var len = jQuery(this).val().length;
    var max = jQuery(this).attr("maxlength");
    jQuery(".count").text("Remaining: " + (max-len));
});

jQuery(document).ready(function(){
    var len = jQuery(".create-post textarea").val().length;
    var max = jQuery(".create-post textarea").attr("maxlength");
    jQuery(".count").text("Remaining: " + (max-len));
});