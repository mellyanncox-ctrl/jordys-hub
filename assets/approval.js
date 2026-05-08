/* ==========================================================================
   APPROVAL FORM HANDLER
   ==========================================================================
   Wires up inline approval forms on review pages.

   Form structure (set up by build.py):
     <form class="approval-form" data-form-id="...">
       <input type="hidden" name="access_key" value="...">
       <input type="hidden" name="subject" value="...">
       <input type="hidden" name="from_name" value="...">
       <input type="text" name="botcheck" class="hp">
       <div class="approval-collapsed">[label + 2 buttons]</div>
       <div class="approval-expanded" hidden>[message + send]</div>
       <div class="approval-thanks" hidden>[checkmark]</div>
     </form>

   Behaviour:
     - Click Approve: expand form, set action=approve, label "Approve"
     - Click Request changes: expand form, set action=changes, label "Request changes"
     - Submit: POST to web3forms.com, on success show thanks block
     - Cancel: collapse form back to default state
   ========================================================================== */

(function () {
  'use strict';

  const ENDPOINT = 'https://api.web3forms.com/submit';

  function setMode(form, mode) {
    const collapsed = form.querySelector('.approval-collapsed');
    const expanded = form.querySelector('.approval-expanded');
    const modeText = form.querySelector('[data-mode-text]');
    const actionInput = form.querySelector('input[name="action"]');
    const message = form.querySelector('.approval-message');
    const status = form.querySelector('[data-status]');

    collapsed.hidden = true;
    expanded.hidden = false;
    actionInput.value = mode;
    status.textContent = '';
    status.classList.remove('is-error');

    if (mode === 'approve') {
      modeText.innerHTML = '<span class="mode-tag is-approve">Approve</span>Add an optional note, or just hit send.';
      message.placeholder = 'Optional message';
      message.required = false;
    } else {
      modeText.innerHTML = '<span class="mode-tag is-changes">Request changes</span>Tell Mel what you\'d like changed.';
      message.placeholder = 'What needs to change?';
      message.required = true;
    }

    setTimeout(() => message.focus(), 50);
  }

  function resetForm(form) {
    const collapsed = form.querySelector('.approval-collapsed');
    const expanded = form.querySelector('.approval-expanded');
    const message = form.querySelector('.approval-message');
    const status = form.querySelector('[data-status]');

    collapsed.hidden = false;
    expanded.hidden = true;
    message.value = '';
    status.textContent = '';
    status.classList.remove('is-error');
  }

  function showThanks(form, action) {
    const collapsed = form.querySelector('.approval-collapsed');
    const expanded = form.querySelector('.approval-expanded');
    const thanks = form.querySelector('.approval-thanks');
    const thanksText = form.querySelector('[data-thanks-text]');

    collapsed.hidden = true;
    expanded.hidden = true;
    thanks.hidden = false;
    thanksText.textContent = action === 'approve'
      ? 'Approved. Mel has been notified.'
      : 'Feedback sent to Mel.';
  }

  async function handleSubmit(form, event) {
    event.preventDefault();

    const status = form.querySelector('[data-status]');
    const sendBtn = form.querySelector('.btn-send');
    const action = form.querySelector('input[name="action"]').value;
    const message = form.querySelector('.approval-message');

    if (action === 'changes' && !message.value.trim()) {
      status.textContent = 'Please describe what needs to change.';
      status.classList.add('is-error');
      message.focus();
      return;
    }

    sendBtn.disabled = true;
    status.classList.remove('is-error');
    status.textContent = 'Sending...';

    const formData = new FormData(form);

    // If approve and no message, fill in a default body so the email isn't empty
    if (action === 'approve' && !message.value.trim()) {
      formData.set('message', 'Approved (no comment).');
    }

    // Append the action to the subject for clarity in the inbox
    const subject = formData.get('subject') || '';
    formData.set('subject', `${subject} | ${action === 'approve' ? 'Approved' : 'Request changes'}`);

    try {
      const response = await fetch(ENDPOINT, {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();

      if (response.ok && result.success) {
        showThanks(form, action);
      } else {
        status.classList.add('is-error');
        status.textContent = (result && result.message) || 'Send failed. Try again or email mel directly.';
        sendBtn.disabled = false;
      }
    } catch (err) {
      status.classList.add('is-error');
      status.textContent = 'Network error. Check your connection and try again.';
      sendBtn.disabled = false;
    }
  }

  function initForm(form) {
    form.addEventListener('click', (e) => {
      const actionBtn = e.target.closest('[data-action]');
      if (actionBtn) {
        setMode(form, actionBtn.dataset.action);
        return;
      }
      if (e.target.closest('[data-cancel]')) {
        resetForm(form);
        return;
      }
    });

    form.addEventListener('submit', (e) => handleSubmit(form, e));
  }

  function init() {
    document.querySelectorAll('.approval-form').forEach(initForm);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
