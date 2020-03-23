# Department for Transport: Road Freight Survey - Alpha project

This repository contains code associated with the Department for Transport's GOV.UK Alpha Phase
for transforming Road Freight Statistics surveys into a Digital Service.

https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities/10964

## User Journey Prototypes

Prototype user journeys for the service were created in a pattern library as static HTML forms.

These are contained in `dft/project_styleguide/templates/patterns/pages`.

The prototypes can be viewed in a [Vagrant](https://www.vagrantup.com/intro/getting-started/install.html) box
from a checkout of this repository.

```
vagrant up
vagrant ssh
djrun
```

The prototypes will then be available at http://locahost:8000

## Notify integration

An integration demo with the GOV.UK Notify service is in `dft/utils/views.py`.

## Machine Learning experiment

An experiment to test the viability of using ML tools to aid data classification is in `ml-experiments`.
