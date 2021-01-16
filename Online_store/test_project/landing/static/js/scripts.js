$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);


    $(function() {
		$('.mask-phone').mask('+7 (999) 999-99-99');
	});

	$(function() {
		$('.mask-email').inputmask("email")
	});



    function basketUpdating(product_id, nmb,  is_delete){
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
//        data.price = price;
        var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete){
            data["is_delete"] = true;
        }

         var url = form.attr("action");

        console.log(data)
         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log("OK");
                 console.log(data.products_total_nmb);
                 if (data.products_total_nmb || data.products_total_nmb == 0){
                    $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                     console.log(data.products);
                     $('.basket-items ul').html("");
                     $.each(data.products, function(k, v){
                       $('.basket-items ul').append('<a class="basket-color" href="/product/'+String(v.id)+'">' + '<li>' + v.name + ' ' + 'Кол-во: ' + v.nmb  + ' по: ' + v.price_per_item + '₽' +
                          '<a class="delete-item basket-color-x" href="" data-product_id ="'+v.id+'">  X</a>' +
                                '</li>' + '</a>');

                         });
                 }

             },
             error: function(){
                 console.log("error")
             }
         })

    }


//        $('#modelWin').submit(function(e) {
//          var empty = $(this).parent().find("input").filter(function() {
//            return this.value === "";
//          });
//          if (!empty.length) {
//            //Если все графы заполнены, то показываем popup
//            $('').show();
//            //очищаем все данные текстовых полей, кроме кнопок
//            $('form input').not(':button, :submit').val('');
//          }
//
//        });
//        $("#modelWin-notAuth").on('submit', function(event) {
//            alert("Спасибо за заказ. В ближайшее время с вами свяжутся!");
////            $(".modal").show();
//         });



    $(document).on('click', '#submit_btn', function(e){
        var form = $(this);
        e.preventDefault();
        var form = $(this);
        console.log('123');
        var nmb = $('#number').val();
        if (nmb == undefined){
            nmb = 1;
        }
        console.log(nmb);
        var product_id = $(this).data("product_id");
        var name = $(this).data("name")
        var price = $(this).data("product-price")

        basketUpdating(product_id, nmb, is_delete=false);

    });

//    $(document).on('click', '#check_btn', function(e){
//       alert('HELLO')
//    });
//
//    function showingBasket(){
//        $('.basket-items').toggleClass('hidden');
//    };

    //$('.basket-container').on('click', function(e){
    //    e.preventDefault();
    //    showingBasket();
    //});

     $('.basket-container').mouseover(function(){
         $('.basket-items').removeClass('hidden');
     });

     $('.basket-container').mouseout(function(){
        $('.basket-items').addClass('hidden');
     });

     $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true);
     });
     $(document).on('click', '#pickupgroup', function(e){

        $('.delivery-address-check').addClass('hidden');
        $('.comments-check').addClass('hidden');


     });
     $(document).on('click', '#couriergroup', function(e){

        $('.delivery-address-check').removeClass('hidden');
        $('.comments-check').removeClass('hidden');



     });




    function calculatingBasketAmount(){
        var total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function() {
            total_order_amount = total_order_amount + parseFloat($(this).text());
        });
        console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };

    $(document).on('change', ".product-in-basket-nmb", function(){
        var current_nmb = $(this).val();
        console.log(current_nmb);
        var current_tr = $(this).closest('tr');
        console.log(current_tr)
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        console.log(current_price);
        var total_amount = parseFloat(current_nmb*current_price).toFixed(2);
        console.log(total_amount);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);

        calculatingBasketAmount();
    });


    calculatingBasketAmount();
});

$(function() {
$(window).scroll(function() {
    if($(this).scrollTop() != 0) {
        $('#toTop').fadeIn();
    } else {
        $('#toTop').fadeOut();
    }
});
    $('#toTop').click(function() {
        $('body,html').animate({scrollTop:0},800);
    });
});
