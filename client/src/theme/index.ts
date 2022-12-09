import { ThemeConfig, extendTheme, withDefaultColorScheme } from '@chakra-ui/react';

const config: ThemeConfig = {
    initialColorMode: 'dark',
    useSystemColorMode: false,
    cssVarPrefix: 'post',
};

const fonts = {
    body: "'Post', sans-serif",
    heading: "'Post', sans-serif",
};

export const theme = extendTheme(
    {
        config,
        fonts,
    },
    withDefaultColorScheme({ colorScheme: 'pink' }),
);
