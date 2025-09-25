"""
Advanced Nutrition Controller
============================

Enterprise-level controller integrating:
- Multi-step nutrition form modal
- Advanced nutrition calculations
- Professional PDF generation
- Real-time validation and UX
- Data persistence and management
"""

from typing import Optional, Dict, Any, Callable
import customtkinter as ctk
from pathlib import Path
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from datetime import datetime
import logging

from ui.modals.nutrition_form_modal import AdvancedNutritionFormModal
from services.advanced_nutrition_calculator import (
    AdvancedNutritionCalculator,
    PersonalData,
    MacroTargets,
    ActivityLevel,
    NutritionGoal,
    NutritionResults,
    BMRMethod
)
from services.professional_nutrition_pdf import generate_professional_nutrition_pdf
from repositories.fiche_nutrition_repo import FicheNutritionRepository
from models.fiche_nutrition import FicheNutrition
from models.client import Client
from exceptions.validation_error import ValidationError

logger = logging.getLogger(__name__)


class AdvancedNutritionController:
    """
    Advanced nutrition controller with premium features.

    Manages the complete nutrition workflow:
    - Client data integration
    - Multi-step form presentation
    - Advanced calculations
    - Professional PDF generation
    - Data persistence and validation
    """

    def __init__(
        self,
        parent_widget,
        fiche_nutrition_repo: FicheNutritionRepository,
        client_service=None
    ):
        self.parent = parent_widget
        self.fiche_repo = fiche_nutrition_repo
        self.client_service = client_service
        self.current_modal = None

        # Coach information for branding
        self.coach_info = {
            'name': 'Coach Professionnel',
            'contact': 'contact@coach-pro.com',
            'logo': None
        }

    def open_nutrition_form_for_client(self, client_id: Optional[int] = None):
        """
        Open advanced nutrition form modal for specific client or new entry.

        Args:
            client_id: Optional client ID to pre-populate form
        """
        try:
            # Get client data if provided
            client_data = None
            if client_id and self.client_service:
                client = self.client_service.get_client_by_id(client_id)
                if client:
                    client_data = {
                        'id': client.id,
                        'nom': client.nom,
                        'prenom': client.prenom,
                        'taille_cm': getattr(client, 'taille_cm', None),
                        'poids_kg': getattr(client, 'poids_kg', None),
                        'date_naissance': getattr(client, 'date_naissance', None),
                        'sexe': getattr(client, 'sexe', None),
                        'niveau_activite': getattr(client, 'niveau_activite', None),
                        'objectifs': getattr(client, 'objectifs', None),
                    }

            # Calculate age from birth date if available
            if client_data and client_data.get('date_naissance'):
                try:
                    from datetime import date
                    birth_date = datetime.strptime(client_data['date_naissance'], '%d/%m/%Y').date()
                    today = date.today()
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                    client_data['age'] = age
                except Exception:
                    pass

            # Open modal with callback
            self.current_modal = AdvancedNutritionFormModal(
                self.parent,
                client_data=client_data,
                save_callback=self._handle_nutrition_results
            )

        except Exception as e:
            logger.error(f"Erreur ouverture formulaire nutrition: {e}")
            self._show_error("Erreur", f"Impossible d'ouvrir le formulaire: {str(e)}")

    def _handle_nutrition_results(self, results: NutritionResults):
        """
        Handle nutrition calculation results - save and generate PDF.

        Args:
            results: Complete nutrition calculation results
        """
        try:
            # Save to database
            fiche_data = self._convert_results_to_fiche(results)
            saved_fiche = self.fiche_repo.add(fiche_data)

            # Generate professional PDF
            self._generate_and_save_pdf(results)

            # Show success message
            self._show_success(
                "Fiche Générée",
                f"Fiche nutrition créée avec succès pour {results.personal_data.prenom} {results.personal_data.nom}"
            )

            # Close modal
            if self.current_modal:
                self.current_modal.destroy()
                self.current_modal = None

        except Exception as e:
            logger.error(f"Erreur sauvegarde fiche nutrition: {e}")
            self._show_error("Erreur Sauvegarde", f"Impossible de sauvegarder: {str(e)}")

    def _convert_results_to_fiche(self, results: NutritionResults) -> FicheNutrition:
        """
        Convert NutritionResults to FicheNutrition model for database storage.

        Args:
            results: Nutrition calculation results

        Returns:
            FicheNutrition object ready for database storage
        """
        return FicheNutrition(
            id=None,
            client_id=getattr(results.personal_data, 'client_id', None),
            date_creation=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            poids_kg_mesure=results.personal_data.poids_kg,
            objectif=results.personal_data.objectif.label,
            proteines_cible_g_par_kg=results.macro_targets.proteines_g_par_kg,
            ratio_glucides_lipides_cible=results.macro_targets.glucides_pct,
            maintenance_kcal=int(results.tdee_kcal),
            objectif_kcal=results.objectif_kcal,
            proteines_g=results.proteines_g,
            glucides_g=results.glucides_g,
            lipides_g=results.lipides_g
        )

    def _generate_and_save_pdf(self, results: NutritionResults):
        """
        Generate professional PDF and save to selected location.

        Args:
            results: Complete nutrition calculation results
        """
        try:
            # Default filename
            client_name = f"{results.personal_data.prenom}_{results.personal_data.nom}"
            default_filename = f"Fiche_Nutrition_{client_name}_{datetime.now().strftime('%Y%m%d')}.pdf"

            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                title="Enregistrer Fiche Nutrition",
                defaultextension=".pdf",
                filetypes=[("Fichiers PDF", "*.pdf")],
                initialname=default_filename
            )

            if not file_path:
                return

            # Generate professional PDF
            generate_professional_nutrition_pdf(
                results=results,
                output_path=file_path,
                coach_info=self.coach_info
            )

            # Show success and offer to open
            response = messagebox.askyesno(
                "PDF Généré",
                f"Fiche nutrition sauvegardée avec succès!\n\n"
                f"Emplacement: {file_path}\n\n"
                f"Voulez-vous ouvrir le fichier maintenant?"
            )

            if response:
                self._open_pdf_file(file_path)

        except Exception as e:
            logger.error(f"Erreur génération PDF: {e}")
            self._show_error("Erreur PDF", f"Impossible de générer le PDF: {str(e)}")

    def _open_pdf_file(self, file_path: str):
        """
        Open PDF file with system default application.

        Args:
            file_path: Path to PDF file
        """
        try:
            import subprocess
            import platform

            if platform.system() == 'Windows':
                subprocess.run(['start', file_path], shell=True, check=True)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', file_path], check=True)
            else:  # Linux and others
                subprocess.run(['xdg-open', file_path], check=True)

        except Exception as e:
            logger.error(f"Erreur ouverture PDF: {e}")
            self._show_error("Erreur", f"Impossible d'ouvrir le PDF: {str(e)}")

    def regenerate_pdf_for_existing_fiche(self, fiche_id: int):
        """
        Regenerate PDF for existing nutrition sheet.

        Args:
            fiche_id: ID of existing nutrition sheet
        """
        try:
            # Get existing fiche
            fiche = self.fiche_repo.get_by_id(fiche_id)
            if not fiche:
                self._show_error("Erreur", "Fiche nutrition introuvable")
                return

            # Get client data
            client = None
            if self.client_service and fiche.client_id:
                client = self.client_service.get_client_by_id(fiche.client_id)

            # Reconstruct results from stored data
            results = self._reconstruct_results_from_fiche(fiche, client)
            if not results:
                self._show_error("Erreur", "Impossible de reconstituer les données")
                return

            # Generate PDF
            self._generate_and_save_pdf(results)

        except Exception as e:
            logger.error(f"Erreur régénération PDF: {e}")
            self._show_error("Erreur", f"Impossible de régénérer le PDF: {str(e)}")

    def _reconstruct_results_from_fiche(
        self,
        fiche: FicheNutrition,
        client: Optional[Client] = None
    ) -> Optional[NutritionResults]:
        """
        Reconstruct NutritionResults from stored FicheNutrition data.

        Args:
            fiche: Stored nutrition sheet
            client: Optional client data

        Returns:
            Reconstructed NutritionResults or None if unable
        """
        try:
            # Reconstruct personal data
            personal_data = PersonalData(
                nom=client.nom if client else "Client",
                prenom=client.prenom if client else "",
                age=self._calculate_age_from_client(client) if client else 30,
                sexe=client.sexe if client and hasattr(client, 'sexe') else "Homme",
                taille_cm=client.taille_cm if client and hasattr(client, 'taille_cm') else 175,
                poids_kg=fiche.poids_kg_mesure,
                niveau_activite=self._parse_activity_level(client),
                objectif=self._parse_nutrition_goal(fiche.objectif)
            )

            # Reconstruct macro targets
            macro_targets = MacroTargets(
                proteines_g_par_kg=fiche.proteines_cible_g_par_kg,
                glucides_pct=fiche.ratio_glucides_lipides_cible,
                lipides_pct=100.0 - fiche.ratio_glucides_lipides_cible
            )

            # Calculate actual percentages
            total_kcal = fiche.proteines_g * 4 + fiche.glucides_g * 4 + fiche.lipides_g * 9
            prot_pct = (fiche.proteines_g * 4 / total_kcal * 100) if total_kcal > 0 else 0
            carb_pct = (fiche.glucides_g * 4 / total_kcal * 100) if total_kcal > 0 else 0
            fat_pct = (fiche.lipides_g * 9 / total_kcal * 100) if total_kcal > 0 else 0

            # Create results object
            return NutritionResults(
                bmr_kcal=fiche.maintenance_kcal / 1.55,  # Estimate BMR from TDEE
                bmr_method=BMRMethod.MIFFLIN_ST_JEOR,
                tdee_kcal=fiche.maintenance_kcal,
                activite_factor=1.55,  # Default moderate activity
                objectif_kcal=fiche.objectif_kcal,
                deficit_surplus=fiche.objectif_kcal - fiche.maintenance_kcal,
                proteines_g=fiche.proteines_g,
                glucides_g=fiche.glucides_g,
                lipides_g=fiche.lipides_g,
                proteines_kcal=fiche.proteines_g * 4,
                glucides_kcal=fiche.glucides_g * 4,
                lipides_kcal=fiche.lipides_g * 9,
                proteines_pct=prot_pct,
                glucides_pct=carb_pct,
                lipides_pct=fat_pct,
                personal_data=personal_data,
                macro_targets=macro_targets
            )

        except Exception as e:
            logger.error(f"Erreur reconstruction données: {e}")
            return None

    def _calculate_age_from_client(self, client: Client) -> int:
        """Calculate age from client birth date"""
        if not client or not hasattr(client, 'date_naissance') or not client.date_naissance:
            return 30  # Default age

        try:
            from datetime import date
            birth_date = datetime.strptime(client.date_naissance, '%d/%m/%Y').date()
            today = date.today()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        except Exception:
            return 30

    def _parse_activity_level(self, client: Optional[Client]) -> ActivityLevel:
        """Parse activity level from client data"""
        if not client or not hasattr(client, 'niveau_activite'):
            return ActivityLevel.SEDENTARY

        activity_str = client.niveau_activite.lower() if client.niveau_activite else ""

        if "légère" in activity_str or "légèrement" in activity_str:
            return ActivityLevel.LIGHTLY_ACTIVE
        elif "modéré" in activity_str:
            return ActivityLevel.MODERATELY_ACTIVE
        elif "très" in activity_str:
            return ActivityLevel.VERY_ACTIVE
        elif "extrême" in activity_str:
            return ActivityLevel.EXTREMELY_ACTIVE
        else:
            return ActivityLevel.SEDENTARY

    def _parse_nutrition_goal(self, objectif_str: str) -> NutritionGoal:
        """Parse nutrition goal from string"""
        if not objectif_str:
            return NutritionGoal.MAINTENANCE

        objectif_lower = objectif_str.lower()

        if "perte" in objectif_lower:
            if "légère" in objectif_lower:
                return NutritionGoal.FAT_LOSS_MILD
            elif "rapide" in objectif_lower:
                return NutritionGoal.FAT_LOSS_AGGRESSIVE
            else:
                return NutritionGoal.FAT_LOSS_MODERATE
        elif "prise" in objectif_lower or "masse" in objectif_lower:
            if "lente" in objectif_lower:
                return NutritionGoal.LEAN_GAIN_SLOW
            elif "rapide" in objectif_lower:
                return NutritionGoal.LEAN_GAIN_AGGRESSIVE
            else:
                return NutritionGoal.LEAN_GAIN_MODERATE
        else:
            return NutritionGoal.MAINTENANCE

    def get_nutrition_history_for_client(self, client_id: int) -> list:
        """
        Get nutrition history for specific client.

        Args:
            client_id: Client ID

        Returns:
            List of nutrition sheets for client
        """
        try:
            return self.fiche_repo.get_all_for_client(client_id)
        except Exception as e:
            logger.error(f"Erreur récupération historique nutrition: {e}")
            return []

    def delete_nutrition_sheet(self, fiche_id: int) -> bool:
        """
        Delete nutrition sheet.

        Args:
            fiche_id: ID of sheet to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            response = messagebox.askyesno(
                "Confirmer Suppression",
                "Êtes-vous sûr de vouloir supprimer cette fiche nutrition?\n\n"
                "Cette action est irréversible."
            )

            if response:
                success = self.fiche_repo.delete(fiche_id)
                if success:
                    self._show_success("Suppression", "Fiche nutrition supprimée avec succès")
                    return True
                else:
                    self._show_error("Erreur", "Impossible de supprimer la fiche")
                    return False

            return False

        except Exception as e:
            logger.error(f"Erreur suppression fiche nutrition: {e}")
            self._show_error("Erreur", f"Erreur lors de la suppression: {str(e)}")
            return False

    def quick_nutrition_calculation(self, client_data: Dict[str, Any]) -> Optional[NutritionResults]:
        """
        Perform quick nutrition calculation without modal.

        Args:
            client_data: Client data dictionary

        Returns:
            NutritionResults or None if error
        """
        try:
            # Create PersonalData from client_data
            personal_data = PersonalData(
                nom=client_data.get('nom', ''),
                prenom=client_data.get('prenom', ''),
                age=client_data.get('age', 30),
                sexe=client_data.get('sexe', 'Homme'),
                taille_cm=client_data.get('taille_cm', 175),
                poids_kg=client_data.get('poids_kg', 70),
                niveau_activite=client_data.get('niveau_activite', ActivityLevel.SEDENTARY),
                objectif=client_data.get('objectif', NutritionGoal.MAINTENANCE)
            )

            # Default macro targets
            macro_targets = MacroTargets()

            # Calculate nutrition
            results = AdvancedNutritionCalculator.calculate_complete_nutrition(
                personal_data, macro_targets
            )

            return results

        except Exception as e:
            logger.error(f"Erreur calcul rapide nutrition: {e}")
            return None

    def set_coach_info(self, coach_info: Dict[str, Any]):
        """
        Set coach information for PDF branding.

        Args:
            coach_info: Dictionary with coach information
        """
        self.coach_info.update(coach_info)

    def _show_success(self, title: str, message: str):
        """Show success message"""
        try:
            messagebox.showinfo(title, message)
        except Exception:
            pass

    def _show_error(self, title: str, message: str):
        """Show error message"""
        try:
            messagebox.showerror(title, message)
        except Exception:
            pass

    def _show_warning(self, title: str, message: str):
        """Show warning message"""
        try:
            messagebox.showwarning(title, message)
        except Exception:
            pass