let stationCount = $(".StationWrapper").length;
for (let index = 0; index < stationCount; index++) {
    $(`#StationHeadButton${index}`).on("click", () => {
        $(`#StationBody${index}`).slideToggle(150);
    });
}