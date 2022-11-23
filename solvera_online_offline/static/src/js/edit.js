odoo.define('solvera_online_offline.purchase', function (require) {
    var FormView = require('web.FormView');
    FormView.include({
     load_record: function() {
      this._super.apply(this, arguments);
      if (this.model === 'purchase.order') {
          if (this.datarecord && (this.datarecord.state === 'purchase')) {
            this.$buttons.find('.o_form_button_edit').css({'display':'none'});
          }
          else {
            this.$buttons.find('.o_form_button_edit').css({'display':''});
          }
       }
    }});
});