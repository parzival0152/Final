function user_only() {
    $(".user-only").removeClass("hidden");
    $(".general-only").addClass("hidden");
}

function general() {
    $(".user-only").addClass("hidden");
    $(".general-only").removeClass("hidden");
}