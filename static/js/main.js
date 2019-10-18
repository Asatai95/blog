// ログイン画面、ラベル横のやつ消す
$(function(){
    $("div label").each(function(){

        $(this).text().replace(":", "");
    });
});

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

    $(".card .row .col.main_box .card-body .card-text.topic span a").each(function(){
        $(this).parents("span").on("mouseover mouseout", function(e){
            if (e.type == "mouseover") {
                $(this).css("box-shadow", "0 0 3px #222");
            }
            if (e.type == "mouseout") {
                $(this).css("box-shadow", "0 0 0");
            }
        });
    });
    $(".card .row .col-md-8 .card-body .card-text.topic span a").each(function(){
        $(this).parents("span").on("mouseover mouseout", function(e){
            if (e.type == "mouseover") {
                $(this).css("box-shadow", "0 0 3px #222");
            }
            if (e.type == "mouseout") {
                $(this).css("box-shadow", "0 0 0");
            }
        });
    });

});

// ページトップスクロールアイコン
$(function(){
    $('.page_top').hide();
    $(window).scroll(function () {
        if($(window).scrollTop() > 0) {
            $('.page_top').slideDown(300);
        } else {
            $('.page_top').slideUp(300);
        }
    });
    $('.page_top').click(function () {
      $("html,body").animate({scrollTop:0}, 1200, 'swing');
    });
    $(".page_top").mouseover(function(){
      $(this).find("img").css("transform", "scale(1.1)");
    });
    $(".page_top").mouseout(function(){
      $(this).find("img").css("transform", "");
    });

  });