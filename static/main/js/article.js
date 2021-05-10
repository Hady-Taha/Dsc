$(function () {
    $(".like").on("submit", function (e) {
        e.preventDefault();
        let postId = $(this).attr("id");
        $.ajax({
            type: "POST",
            url: $(this).data("url"),
            data: $(this).serialize(),
            success: function (response) {
                console.log(response);
                $(".likeCount" + postId).text(response.likeNum);
                $("#like" + postId).attr("class", response.icon + " fa-heart");
            },
        });
    });

    $(".saveArticle").on("submit", function (e) {
        e.preventDefault();
        let postId = $(this).data("id");
        $.ajax({
            type: "POST",
            url: $(this).data("url"),
            data: $(this).serialize(),
            beforeSend: function () {
                $(".spinner-save" + postId).show();
                $(".saveArticleButton" + postId).addClass("disabled");
            },
            complete: function () {
                $(".spinner-save" + postId).hide();
                $(".saveArticleButton" + postId).removeClass("disabled");
            },
            success: function (response) {
                $("#bookmark" + postId).attr("class", response + " fa-bookmark");
            },
        });
    });




});