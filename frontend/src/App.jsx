import { useState, useEffect } from 'react';
import { LogIn, LogOut, Plus, Trash2, Search, Rabbit, Calendar, Weight, User as UserIcon, Heart, Star, Carrot, Home } from 'lucide-react';
import api from './services/api';
import logo from './assets/logo.png';
import defaultRabbit from './assets/default-rabbit.jpg';


export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [fiches, setFiches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [view, setView] = useState('login');
  const [searchTerm, setSearchTerm] = useState('');
  
  const [loginForm, setLoginForm] = useState({ username: 'admin', password: 'adminpass' });
  const [ficheForm, setFicheForm] = useState({
    nom: '',
    numero_arrivee_association: '',
    sexe: 'Mâle',
    poids_actuel: '',
    date_arrivee_association: new Date().toISOString().split('T')[0]
  });

  useEffect(() => {
    if (token) {
      fetchFiches();
    }
  }, [token]);

  const handleLogin = async () => {
    setLoading(true);
    setError('');
    
    try {
      await api.login(loginForm.username, loginForm.password);
      setToken(api.getToken());
      setView('dashboard');
    } catch (err) {
      setError(err.message || 'Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    api.logout();
    setToken(null);
    setView('login');
    setFiches([]);
  };

  const fetchFiches = async () => {
    setLoading(true);
    try {
      const data = await api.getAllFiches();
      setFiches(data);
    } catch (err) {
      if (err.message.includes('401')) {
        handleLogout();
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFiche = async () => {
    setLoading(true);
    setError('');
    
    try {
      const ficheData = {
        ...ficheForm,
        numero_arrivee_association: parseInt(ficheForm.numero_arrivee_association),
        poids_actuel: ficheForm.poids_actuel ? parseInt(ficheForm.poids_actuel) : null,
        date_creation_fiche: new Date().toISOString(),
        date_arrivee_association: new Date(ficheForm.date_arrivee_association).toISOString(),
        auteur_id: 'dummy'
      };
      
      await api.createFiche(ficheData);
      setFicheForm({
        nom: '',
        numero_arrivee_association: '',
        sexe: 'Mâle',
        poids_actuel: '',
        date_arrivee_association: new Date().toISOString().split('T')[0]
      });
      setView('dashboard');
      fetchFiches();
    } catch (err) {
      setError(err.message || 'Erreur lors de la création');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteFiche = async (id) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette fiche ?')) return;
    
    try {
      await api.deleteFiche(id);
      fetchFiches();
    } catch (err) {
      setError(err.message);
    }
  };

  const filteredFiches = fiches.filter(fiche => 
    fiche.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
    fiche.numero_arrivee_association.toString().includes(searchTerm)
  );

  // LOGIN VIEW
  if (view === 'login' || !token) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-100 via-green-50 to-teal-100 flex items-center justify-center p-4 relative overflow-hidden">
        
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-emerald-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-green-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-teal-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
        </div>

        <div className="relative bg-white/80 backdrop-blur-lg rounded-3xl shadow-2xl p-8 w-full max-w-md border border-white/20">
          <div className="text-center mb-8">
            <div className="relative inline-block">
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-500 to-green-500 rounded-full blur-lg opacity-50 animate-pulse"></div>
              <div className="relative bg-white w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 p-2">
                <img src={logo} alt="Logo SPI LOEN" className="w-full h-full object-contain" />
              </div>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
              SPI LOEN
            </h1>
            <p className="text-gray-600 mt-2 flex items-center justify-center gap-2">
              <Carrot className="w-4 h-4 text-orange-500" />
              Console d'administration
              <Carrot className="w-4 h-4 text-orange-500" />
            </p>
          </div>
          
          {error && (
            <div className="bg-red-50/80 backdrop-blur border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-4 animate-shake">
              {error}
            </div>
          )}
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Nom d'utilisateur
              </label>
              <input
                type="text"
                value={loginForm.username}
                onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
                className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                placeholder="admin"
              />
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Mot de passe
              </label>
              <input
                type="password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
                className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                placeholder="••••••••"
              />
            </div>
            
            <button
              onClick={handleLogin}
              disabled={loading}
              className="w-full bg-gradient-to-r from-emerald-600 to-green-600 text-white py-3 rounded-xl font-semibold hover:from-emerald-700 hover:to-green-700 transition-all disabled:opacity-50 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              <LogIn className="w-5 h-5" />
              {loading ? 'Connexion...' : 'Se connecter'}
            </button>
          </div>
          
          <div className="mt-6 p-4 bg-gradient-to-br from-emerald-50 to-green-50 rounded-xl border border-emerald-100">
            <p className="text-sm text-emerald-800 font-semibold flex items-center gap-2">
              <Carrot className="w-4 h-4 text-emerald-500" />
              Comptes de test :
            </p>
            <p className="text-sm text-emerald-500 mt-1">👤 admin / adminpass</p>
            <p className="text-sm text-emerald-500">👤 aurelia/aurelia</p>
          </div>
        </div>
      </div>
    );
  }

  // CREATE VIEW
  if (view === 'create') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50">
        <nav className="bg-white/80 backdrop-blur-lg shadow-lg border-b border-emerald-100">
          <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="bg-white w-10 h-10 rounded-xl flex items-center justify-center p-1">
                <img src={logo} alt="Logo" className="w-full h-full object-contain" />
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
                Nouvelle fiche lapin
              </h1>
            </div>
            <button
              onClick={() => setView('dashboard')}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-white/50 rounded-lg transition-all"
            >
              Annuler
            </button>
          </div>
        </nav>
        
        <div className="max-w-4xl mx-auto p-6">
          {error && (
            <div className="bg-red-50/80 backdrop-blur border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-4">
              {error}
            </div>
          )}
          
          <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl p-8 space-y-8 border border-emerald-100">
            <div className="flex items-center gap-3 pb-4 border-b border-emerald-100">
              <div className="bg-gradient-to-br from-emerald-100 to-green-100 p-3 rounded-xl">
                <Rabbit className="w-6 h-6 text-emerald-600" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-800">Informations du lapin</h2>
                <p className="text-sm text-gray-600">Remplissez les champs obligatoires</p>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <Star className="w-4 h-4 text-emerald-500" />
                  Nom du lapin *
                </label>
                <input
                  type="text"
                  value={ficheForm.nom}
                  onChange={(e) => setFicheForm({...ficheForm, nom: e.target.value})}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                  placeholder="Ex: Pompon"
                />
              </div>
              
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-700">
                  Numéro d'arrivée *
                </label>
                <input
                  type="number"
                  value={ficheForm.numero_arrivee_association}
                  onChange={(e) => setFicheForm({...ficheForm, numero_arrivee_association: e.target.value})}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                  placeholder="123"
                />
              </div>
              
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-700">
                  Sexe *
                </label>
                <select
                  value={ficheForm.sexe}
                  onChange={(e) => setFicheForm({...ficheForm, sexe: e.target.value})}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                >
                  <option>Mâle</option>
                  <option>Femelle</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <Weight className="w-4 h-4 text-emerald-500" />
                  Poids actuel (grammes)
                </label>
                <input
                  type="number"
                  value={ficheForm.poids_actuel}
                  onChange={(e) => setFicheForm({...ficheForm, poids_actuel: e.target.value})}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                  placeholder="2000"
                />
              </div>
              
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-emerald-500" />
                  Date d'arrivée
                </label>
                <input
                  type="date"
                  value={ficheForm.date_arrivee_association}
                  onChange={(e) => setFicheForm({...ficheForm, date_arrivee_association: e.target.value})}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                />
              </div>
            </div>
            
            <div className="flex gap-4 pt-6 border-t border-emerald-100">
              <button
                onClick={handleCreateFiche}
                disabled={loading}
                className="flex-1 bg-gradient-to-r from-emerald-600 to-green-600 text-white py-3 rounded-xl font-semibold hover:from-emerald-700 hover:to-green-700 disabled:opacity-50 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all"
              >
                {loading ? 'Création...' : '🥕 Créer la fiche'}
              </button>
              <button
                onClick={() => setView('dashboard')}
                className="px-8 py-3 bg-white/50 border border-gray-300 rounded-xl hover:bg-white transition-all"
              >
                Annuler
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // DASHBOARD VIEW
  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-green-50 to-teal-50">
      <nav className="bg-white/80 backdrop-blur-lg shadow-lg border-b border-emerald-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-500 to-green-500 rounded-xl blur opacity-50"></div>
              <div className="relative bg-white w-12 h-12 rounded-xl flex items-center justify-center p-1.5">
                <img src={logo} alt="Logo" className="w-full h-full object-contain" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent">
                SPI LOEN
              </h1>
              <p className="text-sm text-gray-600">Console d'administration</p>
            </div>
          </div>
          
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-white/50 rounded-xl transition-all"
          >
            <LogOut className="w-5 h-5" />
            Déconnexion
          </button>
        </div>
      </nav>
      
      <div className="max-w-7xl mx-auto p-6">
        <div className="mb-8 flex flex-col md:flex-row gap-4 justify-between items-start md:items-center">
          <div>
            <h2 className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent flex items-center gap-3">
              <Home className="w-8 h-8 text-emerald-500" />
              Fiches lapins
            </h2>
            <p className="text-gray-600 mt-2 flex items-center gap-2">
              <Carrot className="w-4 h-4 text-orange-600" />
              {fiches.length} petit{fiches.length > 1 ? 's' : ''} compagnon{fiches.length > 1 ? 's' : ''}
            </p>
          </div>
          
          <button
            onClick={() => setView('create')}
            className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-green-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-emerald-700 hover:to-green-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all"
          >
            <Plus className="w-5 h-5" />
            Nouvelle fiche
          </button>
        </div>
        
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-emerald-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Rechercher un lapin par nom ou numéro..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-white/80 backdrop-blur border border-emerald-200 rounded-xl focus:ring-2 focus:ring-emerald-500 outline-none transition-all shadow-md"
            />
          </div>
        </div>
        
        {error && (
          <div className="bg-red-50/80 backdrop-blur border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-4">
            {error}
          </div>
        )}
        
        {loading ? (
          <div className="text-center py-20">
            <div className="relative inline-block">
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-500 to-green-500 rounded-full blur-lg opacity-50 animate-pulse"></div>
              <div className="relative animate-spin rounded-full h-16 w-16 border-4 border-emerald-200 border-t-emerald-600"></div>
            </div>
            <p className="text-gray-600 mt-6 font-medium">Chargement des fiches...</p>
          </div>
        ) : filteredFiches.length === 0 ? (
          <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl p-16 text-center border border-emerald-100">
            <div className="relative inline-block mb-6">
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-300 to-green-300 rounded-full blur-xl opacity-50"></div>
              <Rabbit className="relative w-20 h-20 text-emerald-300" />
            </div>
            <p className="text-gray-600 text-xl mb-4">Aucune fiche trouvée</p>
            <button
              onClick={() => setView('create')}
              className="text-emerald-600 hover:text-emerald-700 font-semibold flex items-center gap-2 mx-auto"
            >
              <Plus className="w-5 h-5" />
              Créer la première fiche
            </button>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredFiches.map((fiche) => (
              <div key={fiche.id} className="group bg-white/80 backdrop-blur-lg rounded-2xl shadow-lg hover:shadow-2xl transition-all overflow-hidden border border-emerald-100 hover:border-emerald-300 transform hover:-translate-y-1">
                {/* Image du lapin */}
                <div className="relative h-48 bg-gradient-to-br from-emerald-100 to-green-100 overflow-hidden">
                  <img 
                    src={fiche.photo && fiche.photo !== '' ? `/photos/${fiche.photo}` : defaultRabbit} 
                    alt={fiche.nom}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    onError={(e) => { e.target.src = defaultRabbit; }}
                  />
                  <div className="absolute top-3 right-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold backdrop-blur-sm ${
                      fiche.sexe === 'Mâle' 
                        ? 'bg-purple-100/80 text-purple-700' 
                        : 'bg-yellow-100/80 text-yellow-700'
                    }`}>
                      {fiche.sexe}
                    </span>
                  </div>
                </div>

                {/* Contenu de la carte */}
                <div className="p-6">
                  <div className="mb-4">
                    <h3 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                      {fiche.nom}
                      <Carrot className="w-5 h-5 text-orange-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </h3>
                    <p className="text-sm text-gray-500 font-medium">N° {fiche.numero_arrivee_association}</p>
                  </div>
                  
                  <div className="space-y-3 text-sm text-gray-600 mb-6">
                    {fiche.poids_actuel && (
                      <div className="flex items-center gap-2 bg-emerald-50 px-3 py-2 rounded-lg">
                        <Weight className="w-4 h-4 text-emerald-500" />
                        <span className="font-medium">{fiche.poids_actuel}g</span>
                      </div>
                    )}
                    <div className="flex items-center gap-2 bg-green-50 px-3 py-2 rounded-lg">
                      <UserIcon className="w-4 h-4 text-green-500" />
                      <span className="font-medium">{fiche.auteur?.username || 'N/A'}</span>
                    </div>
                    {fiche.date_arrivee_association && (
                      <div className="flex items-center gap-2 bg-teal-50 px-3 py-2 rounded-lg">
                        <Calendar className="w-4 h-4 text-teal-500" />
                        <span className="font-medium">{new Date(fiche.date_arrivee_association).toLocaleDateString('fr-FR')}</span>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-2 pt-4 border-t border-emerald-100">
                    <button
                      onClick={() => handleDeleteFiche(fiche.id)}
                      className="flex-1 flex items-center justify-center gap-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-xl transition-all font-medium"
                    >
                      <Trash2 className="w-4 h-4" />
                      Supprimer
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}