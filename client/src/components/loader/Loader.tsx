import { FC } from 'react';

import { Box, Center, Container, Spinner } from '@chakra-ui/react';

export const Loader: FC = () => {
    return (
        <Center w="100%" h="100%" flexDir="column">
            <Container textAlign="center">
                <Spinner size="lg" mb="8" color="pink.500" />
                <Box>Please wait while the API service boots up. This could take about 30s to 1 minute.</Box>
            </Container>
        </Center>
    );
};
