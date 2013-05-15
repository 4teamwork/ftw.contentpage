jQuery(function($){
  var $start = $('div#archetypes-fieldname-startDate');
  var $end = $('div#archetypes-fieldname-endDate');

  $start.bind('calendar_after_change', function(e){
    // Get date infos from start_date field
    var year = $('[id*=year]', $start).attr('value');
    var month = $('[id*=month]', $start).attr('value');
    var day = $('[id*=day]', $start).attr('value');

    // Update them on end_date field, only if end date is empty
    var end_year = $('[id*=year]', $end);
    var end_month = $('[id*=month]', $end);
    var end_day = $('[id*=day]', $end);
    if (end_year.attr('value') === '0000' && end_month.attr('value') === '00' && end_day.attr('value') === '00'){
      $('[id*=year]', $end).attr('value', year);
      $('[id*=month]', $end).attr('value', month);
      $('[id*=day]', $end).attr('value', day);
    }
  });

  var hour = $('select[name="startDate_hour"]');
  var end_hour = $('select[name="endDate_hour"]');
  hour.change(function(){
    if (end_hour.val() == '00') {end_hour.val(hour.val());}
  });
  var minute = $('select[name="startDate_minute"]');
  var end_minute = $('select[name="endDate_minute"]');
  minute.live('change', function(){
    if (end_minute.val() == '00') {end_minute.val(minute.val());}
  });

});
