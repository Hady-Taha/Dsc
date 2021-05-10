var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
    var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("navbar").style.top = "0";
    } else {
        document.getElementById("navbar").style.top = "-100px";
    }
    prevScrollpos = currentScrollPos;
};
AOS.init();

$(function () {
    $(".search").on("submit", function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $(this).data("url"),
            data: $(this).serialize(),
            beforeSend: function () {
                $(".result").empty();
                $(".result").html(`
                <div class="text-center"><div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div></div>`);
            },

            success: function (response) {
                $(".result").empty();
                $(".result").html(response);
            },
        });
    });


    $(".searchInput").on("keyup", function () {
        if ($(this).val()) {
            $(".textSearch").text('In ' + $(this).val());
        }
        if (!$(this).val()) {
            $(".textSearch").text('');
            $.ajax({
                type: "POST",
                url: $(".search").data("url"),
                data: $(".search").serialize(),
                beforeSend: function () {
                    $(".result").empty();
                    $(".result").html(`
                <div class="text-center"><div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div></div>`);
                },
                success: function (response) {
                    $(".result").empty();
                    $(".result").html(response);

                },
            });
        }
    });

});