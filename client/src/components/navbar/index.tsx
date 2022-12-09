import { FC } from 'react';

import {
    Box,
    Button,
    Container,
    Flex,
    Heading,
    Modal,
    ModalBody,
    ModalContent,
    ModalHeader,
    ModalOverlay,
    useDisclosure,
    UseDisclosureProps,
    Text,
    UnorderedList,
    ListItem,
    Stack,
    Divider,
} from '@chakra-ui/react';
import { ReactComponent as PostLogo } from 'assets/logo.svg';

export const AboutModel: FC<UseDisclosureProps> = ({ isOpen, onClose }) => {
    return (
        <Modal isOpen={isOpen!} onClose={onClose!}>
            <ModalOverlay />

            <ModalContent mx="4">
                <ModalHeader>
                    <Heading fontSize="xl">About</Heading>
                </ModalHeader>
                <ModalBody pt="0">
                    <Stack pb="4">
                        <Text>
                            <Text as="span" fontWeight="500">
                                Post
                            </Text>{' '}
                            is a simple algorithm that was developed to tag a word corresponding to its part of speech.
                            The algorithm makes use of a probabilisitic approach along with some randomness, together
                            which forms the basis of an algorithm called Gibbs Sampling. To try it out, just type a
                            sentence in the input box provided below, and click on the button to tag the words!
                        </Text>

                        <Box>
                            <Text>Technology Stack:</Text>
                            <UnorderedList>
                                <ListItem>Python</ListItem>
                                <ListItem>TypeScript</ListItem>
                                <ListItem>Flask</ListItem>
                                <ListItem>React</ListItem>
                            </UnorderedList>
                        </Box>

                        <Divider />

                        <Box>
                            <Button
                                variant="link"
                                onClick={() => window.open('https://github.com/hrishikeshpaul/pos-tagger', '_blank')}
                            >
                                Check out the code on GitHub
                            </Button>
                        </Box>

                        <Text>
                            Developed by{' '}
                            <Button variant="link" onClick={() => window.open('https://iampaul.web.app/', '_blank')}>
                                Hrishikesh Paul
                            </Button>
                        </Text>

                        <br />

                        <Button colorScheme="gray" onClick={onClose}>
                            Close
                        </Button>
                    </Stack>
                </ModalBody>
            </ModalContent>
        </Modal>
    );
};

export const Navbar: FC = () => {
    const { isOpen, onOpen, onClose } = useDisclosure();

    return (
        <>
            <AboutModel isOpen={isOpen} onClose={onClose} />
            <Flex className="post-navbar" bg="white" position="fixed" top="0" w="100%" py="8" px="4">
                <Container maxW="5xl" p="0">
                    <Flex justifyContent="space-between" alignItems="center">
                        <Box width="100px" position="absolute" top="0" pt="4">
                            <PostLogo width="100%" height="100%" />
                        </Box>
                        <Box />
                        <Flex justifyContent="space-between" alignItems="center" gap="8">
                            <Button variant="link" colorScheme="black" onClick={onOpen}>
                                About
                            </Button>
                            <Button variant="link" colorScheme="black">
                                GitHub
                            </Button>
                        </Flex>
                    </Flex>
                </Container>
            </Flex>
        </>
    );
};
