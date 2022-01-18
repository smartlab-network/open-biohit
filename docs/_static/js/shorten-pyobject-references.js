// shorten types like `typing.Any` or `SDF.data_model.parameters.ParameterSet` to `Any` or `ParameterSet`
// only applies if the type is a link to the type object's documentation (so no information is lost)
$(document).ready(function() {
    var spans = $('dl[class^="py"] a[class^="reference"][href] span[class="pre"]');
    spans.each(function() {
        var nameparts = this.innerHTML.split(".")
        this.innerHTML = nameparts[nameparts.length - 1];
    })
})
