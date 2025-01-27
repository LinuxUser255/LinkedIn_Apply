# All the things that need implementing

## More features and functionality needed for comprehensive operation

### Prompts for the methods that handle the "Are you autorized to work in the US" pop-up with 3 drop down menue options  

<br>

**This will need some more editing before the neecessary refactoring is completed.**

```python

def handle_work_authorization(self) -> None:
  try:
    xpath_auth = //*[@id="ember424"]/div/div[2]/form/div/div/h3
```

- For the `handle_work_authorization` method, you are tasked with specific instructions.
- You are to locate and click on a specific  XPath on the webpage.
- You will locate three drop down menus.
- Please follow these instructions carefully, and refactor the `click_next_again_button` method accordingly.
1. **Create a variable named `xpath_work_auth`**
2. **Using the following XPath, set the value for `xpath_work_auth`**
```html
<!-- xpath_work_auth Element -->
<h3 class="t-16 t-bold">
          Additional Questions
        </h3>

<!-- xpath_work_auth xpath -->
//*[@id="ember424"]/div/div[2]/form/div/div/h3

```

```html
<!-- first drop down element selection -->
<!--  -->
<label for="text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-4115470711-11966003578-multipleChoice" class="fb-dash-form-element__label
        fb-dash-form-element__label-title--is-required" data-test-text-entity-list-form-title="">
  <span aria-hidden="true"><!---->Are you authorized to work in the United States on a W2 basis? (No C2C or third-party inquiries)<!----></span><span class="visually-hidden"><!---->Are you authorized to work in the United States on a W2 basis? (No C2C or third-party inquiries)<!----></span>
</label>
<!--First drop down menu xpath -->
//*[@id="ember424"]/div/div[2]/form/div/div/div[1]/div/div/label/span[1]/text()


<!-- second drop down selection Element: Are you a US Citizen or Green Card Holder?* -->
<span aria-hidden="true"><!---->Are you a U.S. Citizen or a Green Card Holder?<!----></span>

<!--second drop down menu xpath: Are you a US Citizen or Green Card Holder?* -->
//*[@id="ember424"]/div/div[2]/form/div/div/div[2]/div/div/label/span[1]


<!-- Third drop down selection Element: -->
<span aria-hidden="true"><!---->Are you currently located in Atlanta, GA, or Nashville, TN?<!----></span>

<!--Third drop down menu xpath:  -->
//*[@id="ember424"]/div/div[2]/form/div/div/div[3]/div/div/label/span[1]

```

