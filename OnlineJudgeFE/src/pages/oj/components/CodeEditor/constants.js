import { keyBy } from 'lodash';

const C = `#include <stdio.h>

int main(void) {
  printf("Hello world!\\n");
  return 0;
}`;

const CPP = `#include <iostream>

int main() {
    std::cout << "Hello world!" << std::endl;
    return 0;
}`;

const JAVA = `public class Main {
  public static void main(String[p] args) {
    System.out.println("Hello world!");
  }
}`;

const JAVASCRIPT = `console.log("Hello world!");`;

const PYTHON = `print("Hello world!")`;

export const CODE_TEMPLATES = {
  C,
  CPP,
  JAVA,
  JAVASCRIPT,
  PYTHON,
};

export const SUPPORT_LANGUAGES = [
  { id: 50, lang: 'c', name: 'C (GCC 9.2.0)', template: CODE_TEMPLATES.C },
  { id: 54, lang: 'cpp', name: 'C++ (GCC 9.2.0)', template: CODE_TEMPLATES.CPP },
  { id: 62, lang: 'java', name: 'Java (OpenJDK 13.0.1)', template: CODE_TEMPLATES.JAVA },
  {
    id: 63,
    lang: 'javascript',
    name: 'Javascript (Node.js 12.14.0)',
    template: CODE_TEMPLATES.JAVASCRIPT,
  },
  { id: 70, lang: 'python', name: 'Python2 (2.7.17)', template: CODE_TEMPLATES.PYTHON },
  { id: 71, lang: 'python', name: 'Python3 (3.8.1)', template: CODE_TEMPLATES.PYTHON },
];
export const DEFAULT_LANGUAGE = 'cpp';
export const DEFAULT_LANGUAGE_CODE = 'C++';
export const DEFAULT_LANGUAGE_ID = 54;
export const LANGUAGES_BY_ID = keyBy(SUPPORT_LANGUAGES, 'id');
export const LANGUAGES_BY_LANG = keyBy(SUPPORT_LANGUAGES, 'lang');
export const LANGUAGES_BY_CODE = keyBy(SUPPORT_LANGUAGES, (item) => item.name.split(' ')[0]);

export const THEMES = ['vs', 'vs-dark', 'hc-black'];
export const DEFAULT_THEME = 'vs';
