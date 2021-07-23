# PyChain Ledger

# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# This is the Record class containing the attributes of the sender, receiver, and amount of each transaction that are included in each block
@dataclass
class Record:
    # Attributes for the Record class
    sender: str
    receiver: str
    amount: float


# This is the Block class containing the Record , creator id, previous hash, timestamp, and nonce attributes. This makes up the Block to be added to the blockchain. 
# This class contains the hash_block() function that runs the sha256 algorithm on the block and returns the hash value
@dataclass
class Block:
    # Attributes for the Block class
    record: Record

    creator_id: int
    prev_hash: str = 0
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: str = 0

    # Function that hashes the block by using the sha256 hashing algorithm
    def hash_block(self):
        sha = hashlib.sha256()

        # hash the record variable in the block
        record = str(self.record).encode()
        sha.update(record)

        # hash the creator_id variable in the block
        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        # hash the timestamp variable in the block
        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        # hash the prev_hash variable in the block
        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        # hash the nonce variable in the block
        nonce = str(self.nonce).encode()
        sha.update(nonce)

        # return the hashed values
        return sha.hexdigest()



# This is the PyChain class containing the entire chain as a List of Blocks. It also contains the difficulty attribute that decides how difficult it is to find the nonce. 
# This class contains the proof_of_work() function that checks that the block can be added to the chain by meeting the required level of difficulty.
# This class contains the add_block function calls the proof_of_work function before adding the block.
# This class contains the is_valid function that check the validity of the blockchain.
@dataclass
class PyChain:
    #Attributes for the chain include the List of Blocks and the difficulty level
    chain: List[Block]
    difficulty: int = 4
    # function to check if the block being added meets the difficulty requirement
    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block
    # function to add the block to the chain
    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]
    # function that checks the valididty of the blockchain
    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True


# Streamlit Code

# Adds the cache decorator for Streamlit so it does not reset


@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])


st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

# Add an input area where you can get a value for `sender` from the user.
sender_input = st.text_input("Enter the name of the sender")

# Add an input area where you can get a value for `receiver` from the user.
receiver_input = st.text_input("Enter the name of the receiver")

# Add an input area where you can get a value for `amount` from the user.
amount_input = st.number_input("Enter the transaction amount")

# Add button for adding new block
if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()


    new_block = Block(
        record=Record(sender_input, receiver_input, amount_input),
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain)
st.write(pychain_df)
#slider for difficulty level
difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())
