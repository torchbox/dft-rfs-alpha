import '@babel/polyfill';
import { initAll } from 'govuk-frontend';

import '../sass/main.scss';

// Worth us only initialising the specific components we use further down the line, but for the sake of speed in Alpha:
initAll();
