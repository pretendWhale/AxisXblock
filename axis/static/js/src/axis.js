/* Javascript for AxisXBlock. */
function AxisXBlock(runtime, element, init_args) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }
    //update the vote counters
    function updateVotes(result) {
        console.log("rating started");
        console.log(result);
        $('.rating.version1', element).text(result.ratingv1);
        $('.num-raters.version1', element).text(result.count_rating_v1);
        // $('.rating.version2', element).text(result.ratingv2);
        // $('.num-raters.version2', element).text(result.count_rating_v2);
    }

    var handlerUrl = runtime.handlerUrl(element, 'update_rating');

    $('.count', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'increment_count'),
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });
//TODO: Make this version agnostic, but make sure that we are sending the correct version to update to the server
$('.rating-button', element).click(function(eventObject) {
    var moocletData = {};
    if (this.classList.contains('version1')) {
        moocletData["version1Rating"] = this.dataset.rating;
    }
    else if (this.classList.contains('version2')) {
        moocletData["version2Rating"] = this.dataset.rating;
    }
    else {
        console.log("error! no version!");
    }
    var rating = this.dataset.rating;
    console.log(moocletData);

        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(moocletData),
            success: updateVotes
        });
    console.log("posted");
    });

    function showVersion(data) {
        var version = data.version;
        $('.hint1').text(version);

    }

    $( document ).ready(function ($) {
        /* Here's where you'd do things on page load. */
        console.log("loaded");

         $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'pick_version_thompson'),
            data: JSON.stringify({"hello": "world"}),
            success: showVersion
        });

         //random selection of version
        // $.ajax({
        //     type: "POST",
        //     url: runtime.handlerUrl(element, 'pick_version_random'),
        //     data: JSON.stringify({"hello": "world"}),
        //     success: showVersion
        // });
    });
    return {};
}
