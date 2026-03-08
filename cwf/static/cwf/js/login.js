var cwf = cwf || {};
cwf.login = (function () {
  const uiSelectors = {};

  function init() {
    uiSelectors.moduleDiv = $("body");
    uiSelectors.moduleDiv.haml(setupLoginUI());
    setupUITriggers();
  }

  function setupLoginUI() {
    return ["%div.page-wrapper", getHeaderUI(), getFormWrapperUI()];
  }

  function getHeaderUI() {
    return [
      "%div.header",
      ["%span.logo-text", "P.  ", ["%span.logo-accent", "Chief"]],
    ];
  }

  function getFormWrapperUI() {
    return [
      "%div.form-wrapper",
      getTabsUI(),
      [
        "%div.forms-container",
        ["%div#sign-in-content", getSignInUI()],
        ["%div#sign-up-content", { style: "display:none;" }, getSignUpUI()],
      ],
    ];
  }

  function getTabsUI() {
    return [
      "%div.tabs-wrapper",
      [
        "%input",
        { type: "radio", id: "sign-in", name: "auth-tabs", checked: "" },
      ],
      ["%label", { for: "sign-in" }, "Sign In"],
      ["%input", { type: "radio", id: "sign-up", name: "auth-tabs" }],
      ["%label", { for: "sign-up" }, "Sign Up"],
      ["%hr.tab-line"],
    ];
  }

  function getSignInUI() {
    return [
      "%form#loginForm",
      { method: "post" },
      [
        "%div.field-group#si-email-div",
        ["%span.input-label", "Email*"],
        ["%input", { type: "text", id: "user_id", name: "user_id" }],
      ],
      [
        "%div.field-group#si-password-div",
        ["%span.input-label", "Password*"],
        ["%input", { type: "password", id: "password", name: "password" }],
      ],
      [
        "%div.btn-wrapper",
        ["%button", { type: "submit", id: "id_login" }, "Sign In"],
      ],
    ];
  }

  function getSignUpUI() {
    return [
      "%div.signup-grid",
      [
        "%div.field-group#su-name-div",
        ["%span.input-label", "Name*"],
        ["%input", { type: "text", id: "su-name" }],
      ],
      [
        "%div.field-group#su-email-div",
        ["%span.input-label", "Email*"],
        ["%input", { type: "text", id: "su-email", autocomplete: "off" }],
      ],
      [
        "%div.field-group#su-password-div",
        ["%span.input-label", "Password*"],
        [
          "%input",
          { type: "password", id: "su-password", autocomplete: "off" },
        ],
      ],
      [
        "%div.field-group#su-cf-password-div",
        ["%span.input-label", "Confirm Password*"],
        [
          "%input",
          { type: "password", id: "su-cf-password", autocomplete: "off" },
        ],
      ],
      [
        "%div.btn-wrapper",
        ["%button", { type: "submit", id: "id_signup" }, "Sign Up"],
      ],
    ];
  }

  // ── Validation ──
  function clearErrors() {
    $(".errors").remove();
  }

  function validateSignIn() {
    clearErrors();
    const email = $("#user_id").val().trim(),
      password = $("#password").val().trim();
    let valid = true;

    if (email === "") {
      valid = false;
      $("#si-email-div").append(
        $("<div class='errors'>Please enter email</div>"),
      );
    } else if (!cwf.utils.validateEmailId(email)) {
      valid = false;
      $("#si-email-div").append(
        $("<div class='errors'>Please enter a valid email</div>"),
      );
    }

    if (password === "") {
      valid = false;
      $("#si-password-div").append(
        $("<div class='errors'>Please enter a password</div>"),
      );
    }

    return valid;
  }

  function validateSignUp() {
    clearErrors();
    const name = $("#su-name").val().trim(),
      email = $("#su-email").val().trim(),
      password = $("#su-password").val().trim(),
      confirmPassword = $("#su-cf-password").val().trim();
    let valid = true;

    if (name === "") {
      valid = false;
      $("#su-name-div").append(
        $("<div class='errors'>Please enter name</div>"),
      );
    }

    if (email === "") {
      valid = false;
      $("#su-email-div").append(
        $("<div class='errors'>Please enter email</div>"),
      );
    } else if (!cwf.utils.validateEmailId(email)) {
      valid = false;
      $("#su-email-div").append(
        $("<div class='errors'>Please enter a valid email</div>"),
      );
    }

    if (password === "") {
      valid = false;
      $("#su-password-div").append(
        $("<div class='errors'>Please enter a password</div>"),
      );
    }

    if (confirmPassword === "") {
      valid = false;
      $("#su-cf-password-div").append(
        $("<div class='errors'>Please re-enter password</div>"),
      );
    } else if (password !== confirmPassword) {
      valid = false;
      $("#su-cf-password-div").append(
        $("<div class='errors'>Passwords do not match</div>"),
      );
    }

    return valid;
  }

  function submitSignUp() {
    const payload = {
      usr_name: $("#su-name").val().trim(),
      usr_email: $("#su-email").val().trim(),
      usr_pswd: $("#su-password").val().trim(),
    };

    $.ajax({
      url: "/onboard-user/",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(payload),
      success: function (response) {
        if (response.status === "success") {
          alert("Account created! Please sign in.");
          $("#sign-in").prop("checked", true);
          $("#sign-up-content").hide();
          $("#sign-in-content").show();
        } else {
          $("#su-email-div").append(
            $("<div class='errors'>" + response.message + "</div>"),
          );
        }
      },
      error: function () {
        alert("Something went wrong. Please try again.");
      },
    });
  }

  // ── UI Triggers ──
  function setupUITriggers() {
    uiSelectors.moduleDiv.on("change", "#sign-in", function () {
      $("#sign-up-content").hide();
      $("#sign-in-content").show();
    });

    uiSelectors.moduleDiv.on("change", "#sign-up", function () {
      $("#sign-in-content").hide();
      $("#sign-up-content").show();
    });

    uiSelectors.moduleDiv.on("click", "#id_login", function (e) {
      e.preventDefault();
      if (validateSignIn()) {
        $("#loginForm").submit();
      }
    });

    uiSelectors.moduleDiv.on("click", "#id_signup", function (e) {
      e.preventDefault();
      if (validateSignUp()) {
        submitSignUp();
      }
    });
  }

  return { init: init };
})();
