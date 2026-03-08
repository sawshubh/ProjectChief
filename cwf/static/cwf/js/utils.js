var cwf = cwf || {};
cwf.utils = (function () {
  function validateEmailId(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  return {
    validateEmailId: validateEmailId,
  };
})();
