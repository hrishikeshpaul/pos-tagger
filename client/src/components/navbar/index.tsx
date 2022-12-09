import { FC } from 'react';

import { Box, Button, Container, Flex } from '@chakra-ui/react';
import { ReactComponent as PostLogo } from 'assets/logo.svg';

export const Navbar: FC = () => {
    return (
        <Flex className="post-navbar" bg="white" position="fixed" top="0" w="100%" py="8" px="4">
            <Container maxW="5xl" p="0">
                <Flex justifyContent="space-between" alignItems="center">
                    <Box width="100px" position="absolute" top="0" pt='4'>
                        <PostLogo width="100%" height="100%" />
                    </Box>
                    <Box />
                    <Flex justifyContent="space-between" alignItems="center" gap="8">
                        <Button variant="link" colorScheme="black">
                            About
                        </Button>
                        <Button variant="link" colorScheme="black">
                            GitHub
                        </Button>
                    </Flex>
                </Flex>
            </Container>
        </Flex>
    );
};
