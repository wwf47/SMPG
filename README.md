# Entity Set Expansion with Meta Path in Knowledge Graph

This codebase contains implementation of the paper:
> Zheng, Yuyan, et al. "Entity set expansion with meta path in knowledge graph." 
> Pacific-Asia conference on knowledge discovery and data mining. 
> Springer, Cham, 2017.
> [[Paper]](https://link.springer.com/chapter/10.1007/978-3-319-57454-7_25)

## Test samples
<p align="center">
  <img src="https://github.com/wwf47/SMPG/blob/main/test.jpg"/ width=200>
</p>

## Running a model
To run the model, execute the following command:
    $ python main.py --seed_dir actor --seed_num 2 
     
Available datasets are:    
    actor
    software
    movie
    scientist
 
## Requirements
The codebase is implemented in Python 3.6. Required packages are:

    numpy    1.19.5
    tqdm     4.62.3
    
## The Proposed Method
### Candidate Entities Extraction
<p align="center">
  <img src="https://github.com/wwf47/SMPG/blob/main/candidate.jpg"/ width=600>
</p>

This method show in `get_candidate.py`. It is used to obtain the candidates based on the seeds.
* Step 1 obtains entity types of each seed. 
* Step 2 generates the initial common candidates types by the intersection operation. 
* Step 3 filters the initial candidates types with the concept hierarchy structure. 
* Step 4 extracts candidate entities satisfying the ultimate candidates types.

### Seed-Based Meta Path Generation
    
