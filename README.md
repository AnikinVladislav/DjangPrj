# DjangPrj

VE_fin_app - venv + django project where i study django (Test)

fin_venv - venv + django project where i work on diplom work 


Try later: 

Save model:
state = {
    'epoch': epoch,
    'state_dict': model.state_dict(),
    'optimizer': optimizer.state_dict()
}
torch.save(state, filepath)

Resume training after load:
model.load_state_dict(state['state_dict'])
optimizer.load_state_dict(state['optimizer'])
