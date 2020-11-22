// https://gist.github.com/belsrc/672b75d1f89a9a5c192c

export default async ({ Vue }) => {
  const currency = function(amount) {
    const amt = Number(amount);
    return (
      (amt && amt.toLocaleString(undefined, { maximumFractionDigits: 4 })) ||
      "-"
    );
  };
  Vue.filter("currency", currency);

  Vue.filter("percentage", function(value, decimals) {
    if (!value) {
      value = 0;
    }

    if (!decimals) {
      decimals = 0;
    }

    value = value * 100;
    value = Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals);
    value = value + "%";
    return value;
  });
};
