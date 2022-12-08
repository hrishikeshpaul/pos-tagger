import { ThemeConfig, extendTheme, withDefaultColorScheme } from '@chakra-ui/react';

const config: ThemeConfig = {
    initialColorMode: 'light',
    useSystemColorMode: false,
    cssVarPrefix: 'post',
};

const fonts = {
    body: "'Plus Jakarta Sans', sans-serif",
    heading: "'Plus Jakarta Sans', sans-serif",
};

const fontWeights = {
    hairline: 100,
    thin: 200,
    light: 300,
    normal: 500,
    medium: 600,
    semibold: 700,
    bold: 800,
    extrabold: 900,
    black: 900,
};

export const theme = extendTheme(
    {
        config,
        fonts,
        fontWeights,
    },
    withDefaultColorScheme({ colorScheme: 'pink' }),
);
