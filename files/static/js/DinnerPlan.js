/**
 * Created by hakloev on 07/05/2016.
 */

var DinnerPlan = (function ($) {
    
    var recipes;
    var days = [
        {id: 0, title: 'Monday' },
        {id: 1, title: 'Tuesday'},
        {id: 2, title: 'Wednesday'},
        {id: 3, title: 'Thursday'},
        {id: 4, title: 'Friday'},
        {id: 5, title: 'Saturday'},
        {id: 6, title: 'Sunday'}
    ];

    var addMealTemplate = [
        '<tr id="item-<%= id %>">',
        '<input id="id_items-<%= id %>-plan" name="items-<%= id %>-plan" type="hidden"><input id="id_items-<%= id %>-id" name="items-<%= id %>-id" type="hidden">',
        '<input id="id_items-<%= id %>-plan" name="items-<%= id %>-plan" type="hidden"><input id="id_items-<%= id %>-id" name="items-<%= id %>-id" type="hidden">',
        '<td><select class="recipe-select2" id="id_items-<%= id %>-recipe" name="items-<%= id %>-recipe">',
        '<% _.each(recipes, function(r) { %>',
        '<option value="<%= r.pk %>"><%= r.title %></option>',
        '<% }); %>',
        '</select></td>',
        '<td><select class="day-select2" id="id_items-<%= id %>-day" name="items-<%= id %>-day">',
        '<% _.each(days, function(d) { %>',
        '<option value="<%= d.id %>"><%= d.title %></option>',
        '<% }); %>',
        '</select></td>',
        '<td><label class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" for="id_items-<%= id %>-eaten"><input class="mdl-checkbox__input" id="id_items-<%= id %>-eaten" name="items-<%= id %>-eaten" type="checkbox"></label></td>',
        '<\/tr>'
    ].join('');

    var addRecipeTemplate = [
        
    ].join('');

    var getRecipes = function () {
        $.ajax({
            url: '/food/recipe/all/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                recipes = data;
            },
            error: function (err) {
                console.log(err);
            }
        });
    };

    var changeEaten = function (data) {
         $.ajax({
            url: '/food/meal/edit/',
            type: 'POST',
            data: data,
            success: function (data) {

            },
            error: function (err) {
                console.log('[ERROR]: Eaten value could not be changed');
                console.log(err);
            }
        });
    };

    var bindListeners = function () {
         $('.add-meal').click(function (e) {
            e.preventDefault();
            var count = $('.hn-food-table__body').children().length;
            var templateMarkup = addMealTemplate;
            var compiledTemplate = _.template(templateMarkup)({ id : count, recipes: recipes, days: days });
            $('tbody.hn-food-table__body').append(compiledTemplate);
            $('#id_items-TOTAL_FORMS').attr('value', count + 1);
            $('#id_items-' + count + '-recipe').select2();
            $('#id_items-' + count + '-day').select2();
            console.log(count);
            componentHandler.upgradeDom(); // In order to upgrade mdl-checkbox
            if (count == 6) {
                $('.add-meal').remove();
            }
        });

        $('.meal-checkbox').change(function (e) {
            var pk = $(e.target).attr('id').split('-')[2];
            var checked = ($(e.target).is(':checked') === true) ? 1 :0;
            changeEaten({'value': checked, 'pk': pk});
        });
    };

    var startSelect2 = function () {
        $('.recipe-select2').select2();
        $('.day-select2').select2();
    };

    return {
        init: function() {
            getRecipes();
            bindListeners();
            startSelect2();
        }
    }
    
})(jQuery);

$(document).ready(function () {
    if ($('#hn-food').length) {
        DinnerPlan.init();
    }
});