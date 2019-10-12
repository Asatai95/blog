
$(function(){
    $(window).on("scroll", function(){
        var scrollPosition = $(window).height() + $(window).scrollTop();
        var scrollHeight = $(document).height();
        if (scrollHeight - scrollPosition == 0) {
            $("footer").fadeIn(800);
        } else {
            $("footer").hide();
        }
    });
    var tmp_list = [];
    var random = Math.floor( Math.random() * (6 - 0) ) + 0;
    tmp_list.push(random)
    var random_max = Math.floor( Math.random() * (10 - 6) ) + 6;
    tmp_list.push(random_max)
    console.log(tmp_list)
    var tmp_count_list = [];
    $(".article_text_link").removeClass("active");
    $(".article_text_link").each(function(index){
        tmp_count_list.push(index)
        if (index == tmp_list[0] || index == tmp_list[1]){
            $(this).addClass("active");
        }
    });
    if (tmp_count_list.length > 4) {
        $(".bottom_article_tile_link").css("height", "750px");
    }

    $(".article_text_link").each(function(){
        $(this).on("click", function(){
            var link = $(this).find("a").attr("href");
            window.location.href = link;
        });
    });
});