window.onload = Main;

function Main(){
    ActiveCopyButtons('.copy_button');

    $(function() {
        moment.locale('ru');
        $('.date-range-picker').each(function() {
            let $this = $(this);

            let drops = $this.data('drops') || 'down';
            let single = $this.data('single') || false;

            $this.daterangepicker({
                autoUpdateInput: false,
                singleDatePicker: single,
                drops: drops,
                linkedCalendars: false,
                showDropdowns: true,
                locale: {
                    cancelLabel: 'Clear'
                },
                buttonClasses: 'btn',
                applyButtonClasses: 'btn-success',
                cancelButtonClasses: 'btn-secondary',
            });

            let dateFormat = 'DD.MM.YYYY';
            if (single){
                $this.on('apply.daterangepicker', function(ev, picker) {
                    $(this).val(picker.startDate.format(dateFormat))
                });
            }else{
                $this.on('apply.daterangepicker', function(ev, picker) {
                    $(this).val(picker.startDate.format(dateFormat) + ' - ' + picker.endDate.format(dateFormat));
                });
            }

            $this.on('cancel.daterangepicker', function(ev, picker) {
                $(this).val('');
            });
        });
    });
}
function ActiveCopyButtons(classname){  // copy text of previos subling
    let buttons = document.querySelectorAll(classname);
    Array.from(buttons).forEach(button => {
        button.onclick = ()=>{
            if(button.previousElementSibling != null){
                navigator.clipboard.writeText(button.previousElementSibling.innerText).then(
                    () => {
                    /* clipboard successfully set */
                    AddClassOnTime(button, 'copy-alert');
                    },
                    () => {
                    /* clipboard write failed */
                    },
                )
            }
        };
    });
}
function AddClassOnTime(element, classlist = "", time = 1000){
    element.classList.add(classlist);
    setTimeout(()=>{element.classList.remove(classlist)},time);
}

